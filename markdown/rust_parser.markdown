% Writing a Simple Parser in Rust
% Adrian Neumann (adrian_neumann@gmx.de)

In an effort to learn Rust I wrote a parser for simple arithmetic expressions. I want to parse expressions of the form `1234 + 43* (34 +[2])` using a simple recursive descent parser. Maybe I'll try one of the libraries for writing parsers next. [Nom](https://github.com/Geal/nom) looks good.

First I define a grammar for my language. To refresh my memory about how grammars for arithmetic expressions should look like, I consult [this site](http://pages.cs.wisc.edu/~fischer/cs536.s08/course.hold/html/NOTES/3.CFG.html#exp). I want `*` to have higher precedence than `+` and of course expressions in parentheses should have higher precedence still.

The grammar I came up with is as follows:

~~~~~~~
   expr -> summand + expr | summand
   summand -> term * expr | term
   term -> NUMBER | ( expr )
~~~~~~~

Next I want define a type for items in this grammar. Normally I'd use inheritance, but Rust doesn't have inheritance, so instead I use an `enum`. Enums in Rust are very useful because unlike in C I can add information to an enum value. For my grammar items, I add the value of the `NUMBER` terminal to the corresponding enum value.

~~~~~~~
#[derive(Debug)]
enum GrammarItem {
    Product,
    Sum,
    Number(i64),
    Paren
}
~~~~~~~

The nodes of my parse tree are structs that contain a `GrammarItem` and children in a vector like so

~~~~~~~
#[derive(Debug)]
struct ParseNode {
    children: Vec<ParseNode>,
    entry: GrammarItem,
}

impl ParseNode {
    pub fn new() -> ParseNode {
        ParseNode {
            children: Vec::new(),
            entry: GrammarItem::Paren,
        }
    }
}
~~~~~~~

I know that each node can have at most two children, so a vector of children is probably overkill. But by using a vector I don't have to worry about using `Box` to avoid [recursive types](https://stackoverflow.com/q/25296195).

Usually one parses by first lexing the input and then constructing the parse tree. My parse function hence looks like this:

~~~~~~~~
fn parse(input: &String) -> Result<ParseNode, String> {
    let tokens = try!(lex(input));
    parse_expr(&tokens, 0).and_then(|(n, i)| if i == tokens.len() {
        Ok(n)
    } else {
        Err(format!("Expected end of input, found {:?} at {}", tokens[i], i))
    })
}
~~~~~~~~

Parsing can fail, so I return a `Result`. I first attempt to lex the input using the `lex` function, which I will show you in a moment. Lexing can also fail, so `lex` also returns a `Result`. At first I had a `match` on the return value of `lex`, so that I could call the parsing function only upon success, but then I learned about the `try!` macro. That's a neat helper function that takes a `Result` and unwraps it if it's ok and otherwise returns the error.

If the lexing succeeds I stuff the tokens into the `parse_expr` function. The second parameter tells the function that it should start at the beginning. Since parsing can fail, `parse_expr` also returns a Result. In the success case, it returns a parse tree and an index one-past the last token it consumed. It can happen that the `parse_expr` function manages to construct a parse tree, but doesn't consume all input. For example for the input string `(1+2)(3+4)` we manage to parse the `(1+2)` prefix, but then get stuck. In the success case, I want to check that the index returned indicates that we consumed all tokens. This doesn't happen in the `parse_expr` function itself, because I want to use it recursively to parse the `( expr )` production in the grammar. In that case it is expected to stop parsing before consuming the closing `)`.

This time I use the `and_then` function of the `Result` type to continue the computation if parsing was successful (I think I could have used another `try!` if I wanted to. I don't know enough Rust to say which is more idiomatic). The closure that I put into `and_then` gets the `ParseNode` `n` and the index `i`. If the index is too small, I error out. The error message is constructed using the `format!` macro.

Let's move on to lexing. The `lex` function gets a `String` and turns it into a vector of tokens. So first I define another type for tokens. Again I use an enum.

~~~~~~~
#[derive(Debug, Clone)]
enum LexItem {
    Paren(char),
    Op(char),
    Num(i64),
}
~~~~~~~

I could have used more enum values to distinguish between `+` and `*` and the different types of parentheses, but instead I just store the character. It probably would have been a good idea to add another integer to each `LexItem` that stores the location in the input at which the token starts. That would make error reporting more useful. Instead I will just use the position in the token stream for my errors. Since I'm the only user of this program, I will only be angry at myself, so it's okay.

The language I want to parse is very simple to lex. Except numbers, all tokens are just a single character long. So instead of complicated things with regular expressions. Instead I iterate over the characters of my input `String` and use a `match` do create a `LexItem`. The `match` statement is really handy here, since I can specify multiple alternatives for the same case with `|` and ranges of characters are also supported.

~~~~~~~~
fn lex(input: &String) -> Result<Vec<LexItem>, String> {
    let mut result = Vec::new();

    let mut it = input.chars().peekable();
    while let Some(&c) = it.peek() {
        match c {
            '0'...'9' => {
                it.next();
                let n = get_number(c, &mut it);
                result.push(LexItem::Num(n));
            }
            '+' | '*' => {
                result.push(LexItem::Op(c));
                it.next();
            }
            '(' | ')' | '[' | ']' | '{' | '}' => {
                result.push(LexItem::Paren(c));
                it.next();
            }
            ' ' => {
                it.next();
            }
            _ => {
                return Err(format!("unexpected character {}", c));
            }
        }
    }
    Ok(result)
}
~~~~~~~~

I have the feeling that this method could be improved so that the vector doesn't have to be mutable and is instead constructed directly using something like `collect`. I Python I would have written a generator from the loop and collected all `yield`-ed items in a list. If it were sufficient to consume only single characters, I could use `map` and `collect` to build my vector. But since `get_number` eats a whole number, I'm not sure how to do it.

I'm not particularly happy about this function because I need a `peekable` iterator and I call `next()` so often. I would prefer to call `next` only in the `while`, but I couldn't figure out a way that lets `get_number` consume a whole number without consuming the first character *after* the number as well. If I were to call `next` in the beginner of the loop, I wouldn't see that character.

For the same reason I can't use `take_while` to get only the part of the iterator that contains digits into `get_number`. That function would hide the character after the number from my lexer.

To extract a number from the input I use the following function.

~~~~~~~~
fn get_number<T: Iterator<Item = char>>(c: char, iter: &mut Peekable<T>) -> i64 {
    let mut number = c.to_string().parse::<i64>().expect("The caller should have passed a digit.");
    while let Some(Ok(digit)) = iter.peek().map(|c| c.to_string().parse::<i64>()) {
        number = number * 10 + digit;
        iter.next();
    }
    number
}
~~~~~~~~

Here again I can't use `next` in the `while` because I don't want to consume the first non-digit, like `take_while` would. Instead I only `peek` at the next character. I use `map` to attempt a parsing of the digit into an int only in the `Some` case without having to do another `if let`. In case of `None` from the `peek`, `map` is a no-op. Maybe I should do some calculations involving the ASCII value of `c`, or alternatively extract the whole number as a slice and `parse` that to be more efficient.

The next step is to actually start constructing the parse tree. As I said above, I use the `parse_expr` function for a simple recursive descent. It looks like this:

~~~~~~~~
fn parse_expr(tokens: &Vec<LexItem>, pos: usize) -> Result<(ParseNode, usize), String> {
    let (node_summand, next_pos) = try!(parse_summand(tokens, pos));
    let c = tokens.get(next_pos);
    match c {
        Some(&LexItem::Op('+')) => {
            // recurse on the expr
            let mut sum = ParseNode::new();
            sum.entry = GrammarItem::Sum;
            sum.children.push(node_summand);
            let (rhs, i) = try!(parse_expr(tokens, next_pos + 1));
            sum.children.push(rhs);
            Ok((sum, i))
        }
        _ => {
            // we have just the summand production, nothing more.
            Ok((node_summand, next_pos))
        }
    }
}
~~~~~~~~

Instead of an iterator I use an index into the vector. I found this easier because `usize` can be copied around implicitly and I have no trouble with the borrow-checker. I first attempt to parse a summand with `parse_summand`. This returns a `Result`. I use `try!` to continue the computation if it succeeds. If I successfully parsed a summand, I check whether the next token is a `+`. I that case I need to parse the RHS of the `+` recursively. The function to parse a summand looks very similar.

~~~~~~~~
fn parse_summand(tokens: &Vec<LexItem>, pos: usize) -> Result<(ParseNode, usize), String> {
    let (node_term, next_pos) = try!(parse_term(tokens, pos));
    let c = tokens.get(next_pos);
    match c {
        Some(&LexItem::Op('*')) => {
            // recurse on the expr
            let mut product = ParseNode::new();
            product.entry = GrammarItem::Product;
            product.children.push(node_term);
            let (rhs, i) = try!(parse_expr(tokens, next_pos + 1));
            product.children.push(rhs);
            Ok((product, i))
        }
        _ => {
            // we have just the term production, nothing more.
            Ok((node_term, next_pos))
        }
    }
}
~~~~~~~~

I suppose I could have abstracted a bit, but I don't know whether the reduced code duplication would have been worth the increased complexity.

The function to parse a term looks most complicated, because this is where I generate all my more or less helpful error messages.

~~~~~~~
fn parse_term(tokens: &Vec<LexItem>, pos: usize) -> Result<(ParseNode, usize), String> {
    let c: &LexItem = try!(tokens.get(pos)
        .ok_or(String::from("Unexpected end of input, expected paren or number")));
    match c {
        &LexItem::Num(n) => {
            let mut node = ParseNode::new();
            node.entry = GrammarItem::Number(n);
            Ok((node, pos + 1))
        }
        &LexItem::Paren(c) => {
            match c {
                '(' | '[' | '{' => {
                    parse_expr(tokens, pos + 1).and_then(|(node, next_pos)| {
                        if let Some(&LexItem::Paren(c2)) = tokens.get(next_pos) {
                            if c2 == matching(c) {
                                // okay!
                                let mut paren = ParseNode::new();
                                paren.children.push(node);
                                Ok((paren, next_pos + 1))
                            } else {
                                Err(format!("Expected {} but found {} at {}",
                                            matching(c),
                                            c2,
                                            next_pos))
                            }
                        } else {
                            Err(format!("Expected closing paren at {} but found {:?}",
                                        next_pos,
                                        tokens.get(next_pos)))
                        }
                    })
                }
                _ => Err(format!("Expected paren at {} but found {:?}", pos, c)),
            }
        }
        _ => {
            Err(format!("Unexpected token {:?}, expected paren or number", {
                c
            }))
        }
    }
}
~~~~~~~

The function is a lot simpler than the deep nesting makes it seem. We just check whether the next token is a number or a parenthesis. If it's a number we simply return it. If it's a parenthesis we parse the contained expression recursively and then check that the next token is a matching closing parenthesis. The function `matching` returns the matching parenthesis using a simple `match`

~~~~~~~
fn matching(c: char) -> char {
    match c {
        ')' => '(',
        ']' => '[',
        '}' => '{',
        '(' => ')',
        '[' => ']',
        '{' => '}',
        _ => panic!("should have been a parenthesis!"),
    }
}
~~~~~~~

The last thing we need for this simple parser is a way to supply it with input. I use a the command line argument as input. The `main` function looks like this.

~~~~~~~
use std::env;

fn main() {
    let args: Vec<_> = env::args().collect();
    if args.len() > 1 {
        println!("The first argument is {}", args[1]);
        println!("{:?}", parse(&args[1]));
    }
}
~~~~~~~

The output is not terribly pretty:

~~~~~~~
$ ./main "1234 + 43* (34 +[2])"
The first argument is 1234 + 43* (34 +[2])
Ok(ParseNode { children: [ParseNode { children: [], entry: Number(1234) }, ParseNode {
children: [ParseNode { children: [], entry: Number(43) }, ParseNode { children: [ParseNode {
children: [ParseNode { children: [], entry: Number(34) }, ParseNode { children: [ParseNode {
children: [], entry: Number(2) }], entry: Paren }], entry: Sum }], entry: Paren }], entry:
Product }], entry: Sum })
~~~~~~~

If you properly indent it, it looks like this:

~~~~~~~
Ok(
  ParseNode {
    children: [
    	ParseNode { children: [], entry: Number(1234) },
    	ParseNode { children: [
	    		ParseNode { children: [], entry: Number(43) },
	    		ParseNode { children: [
	    			ParseNode { children: [
		    				ParseNode { children: [], entry: Number(34) },
		    				ParseNode { children: [
			    					ParseNode { children: [], entry: Number(2) }
			    				],
			    				entry: Paren
		    				}],
	    				entry: Sum
	    			}],
  			entry: Paren
    		}],
  		entry: Product
    	}],
  	entry: Sum })
~~~~~~~

It is very simple to write a pretty-printer for `ParseNode`. It's just a combination of `match` and `format!`

~~~~~~~
fn print(tree: &ParseNode) -> String {
    match tree.entry {
        GrammarItem::Paren => {
            format!("({})",
                    print(tree.children.get(0).expect("parens need one child")))
        }
        GrammarItem::Sum => {
            let lhs = print(tree.children.get(0).expect("sums need two children"));
            let rhs = print(tree.children.get(1).expect("sums need two children"));
            format!("{} + {}", lhs, rhs)
        }
        GrammarItem::Product => {
            let lhs = print(tree.children.get(0).expect("products need two children"));
            let rhs = print(tree.children.get(1).expect("products need two children"));
            format!("{} * {}", lhs, rhs)
        }
        GrammarItem::Number(n) => format!("{}", n),
    }
}
~~~~~~~

After integrating that function into `main`, the output is readable again:

~~~~~~~~
$ ./main "1234 + 43* (34 +[2])"
The first argument is 1234 + 43* (34 +[2])
Ok(ParseNode { children: [ParseNode { children: [], entry: Number(1234) }, ParseNode {
children: [ParseNode { children: [], entry: Number(43) }, ParseNode { children: [ParseNode {
children: [ParseNode { children: [], entry: Number(34) }, ParseNode { children: [ParseNode {
children: [], entry: Number(2) }], entry: Paren }], entry: Sum }], entry: Paren }], entry:
Product }], entry: Sum })
1234 + 43 * (34 + (2))
~~~~~~~~

The next step is testing the parser properly using QuickCheck. I'll do that next and update this article.