# Java Basics 

Before you begin trying to make a Minecraft mod, it is important that you are comfortable with the Java programming language. There exist better ways to learn Java for beginners than this document but I'll make an attempt. If you've already got a good understanding of Java, I encourage you to skip this and get started making your mod. Otherwise, if you're already comfortable with another programming language, this will be trivial to learn, if not might be kinda difficult. 

If you're new to programming, I recommend you follow along and experiment with my examples. If you don't have java installed on your computer yet, you can use an [online compiler](https://www.onlinegdb.com/online_java_compiler) to run your programs without leaving your web browser. 

I promise this will be the longest and most boring page on this site. 

## Primitive Types

Every piece of information your programs can store has a type. Simple data types are called primitives and are the building blocks of more complex types

- `boolean`, can either store `true` or `false`
- `byte`, can store values of `-128` to `127`  
- `short`, can store value of `-32768` to `32767` 
- `int`, can store value of `-2147483648` to `2147483647`
- `long`, can store value of `-9223372036854775808` to `9223372036854775807`
- `char`, can store characters
- `float`, can store decimal numbers
- `double`, can store a wider range of decimal numbers

Although a `long` can hold much more data than a `byte`, you may choose to use a smaller data type when you can predict the range of your data because is saves memory. When you have a variable whose value you know will never go over 127, there's no reason to use 4 times the memory for an `int`. In practice, modern computers are powerful enough that it almost never actually matters.

## Variables

A variable holds one piece of information. They have a type, a name, and a value.

When you declare a variable, you first state the type you want to use and then the name for the variable. 

    int foo;

To declare multiple variables with the same type:

```
int foo, foo1, foo2;
```

Every statement (such as a declaration, assignment, method call) must end with a `;` character. The convention is to keep each statement on its own line of code.

When you declare a variable with a primitive type without assigning it a value, it will default to `0`.

To give our variable a value other than the default we can initialize it with a value:

    int foo = 1;

Or, first declare the variable and later in the code give it a value to store:

    int foo;
    foo = 1;

When you declare a float, double or long typed variable you must follow the number with a letter that represents the type. 

```
double a = 1.5d;
float b = 4f;
long c = 1234L;
```

## Comments 

Any text on a line past `//` is ignored by the complier. This is called a comment. They can be used to describe the thought process behind your code to make it easier to read.

Multi-line comments can be made by putting anything between `/*` and `*/`

```
/* this is not code
it will be ignored */

int foobar = 4; // also a comment
```

## Operators

Operators act between two values. The five arithmetic operators are fairly self explanatory:

- +,  addition 
- -,  subtraction 
- *, multiplication 
- /,  division 
- %, modulo (remainder) 

These operators can be only used while working with primitive types. The only exception is a string concatenation, when we want to combine two sequences of characters into one String.

    int foo = 1;
    int bar = 2;
    
    int result = foo + bar; 

Now result stores the value 3. In this case, the variables `foo` and `bar` are redundant. This is an equivalent statement: 

    int result = 1 + 2;

Of course, the other operators work the same way. 

    double speed = 1.0 / 8.0; // speed is now 0.125
    double four = speed * 32;
    
    // modulo gives the remainder of a devision
    int thing = 12 % 10; // thing is 2
    
    // delare a string by putting text in quotes
    String name = "Luke";
    String greeting = "Hi " + name;

The modulo operator (`%`) gives the remainder when the first number is divided by the second. For example, 

```
int baz = 10 % 3; // 1
// 10 devided 3 is 3 with a remainder of 1

int bar = 100 % 7; // 2
// 100 devided by 7 is 14 with a remainder of 2
```



There are 3 boolean operators.

- `!`, not, which inverts the value
- `&&`, and, which checks that both of the values are true
- `||`, or, which checks that at least one of the values is true

    boolean foo = true;
    boolean bar = !foo;  // false
    boolean baz = foo && bar; // false
    boolean bam = foo || bar; // true

There are 6 types of equality operator. They are used to compare 2 numbers and evaluate to a boolean. 

- `==`, compares a value when used on primitive types and a reference when used on reference types 

- `!=`, is not equal to (inverse of ==) 

- `>`, is greater than 

- `>=`, is greater than or equal 

- `<`, is less than 

- `<=`, is less than or equal 

```
boolean foo = 3 > 1; // true
boolean bar = 9 == (3 + 4); // false
```

`instanceof` is used for checking if an object is an instance of a particular class or it's subtype. This will make more sense once we learn more about objects. Example,

    String foo = "hello world";
    boolean result = foo instanceof String; // true
    boolean other = foo instance of ArrayList; // false

Operators that evaluate to booleans can be chained together to form boolean expressions. These expressions can anywhere a boolean is needed.

    boolean foo = 1 < 2 || 2 < 1;

`foo` will hold the value `true`, even though the second expression returns `false`. Because at least the expression on the right returned `true`.

    boolean bar = 1 < 2 && 2 < 1;

`bar` however, will be `false` because only one of the expressions was `true`.

## Output Text

The simplest way for your program to display information to the user is:

```
System.out.println("Hello World");
System.out.println(10 * 2 + 5);
```

Whatever you pass in to that function call will be printed to the console. 

## If Statements

An if statement controls the flow of your program. You can specify code to run only if a boolean expression (known as a condition in this context) is true. 

    int foo = 5;
    int bar = 10;
    
    if (bar > foo) {
       // run some code
    }

### Else 

You may find your self wanting to run another block of code only if your condition is false. You could do something like this,

```
if (condition){
    runCode();
}
if (!condition){
    runOtherCode();
}
```

But there's a less verbose way:

```
if (condition){
    runCode();
} else {
    runOtherCode();
}
```

### If Else

You may find your self wanting to check anther condition only if the first was false. You could do something like this:

```
if (condition){
    runCode();
} else {
    if (otherCondition){
        runOtherCode();
    } else {
        if (thirdCondition){
            thingOne();
        } else {
            thingTwo();
        }
    }
}
```

But there's a more clear way:

```
if (condition){
    runCode();
} else if (otherCondition){
    runOtherCode();
else if (thirdCondition){
    thingOne();
} else {
    thingTwo();
}
```

Remember, as soon as one of the conditions evaluates to true, that block will execute and none of the lower ones will.  

less levels of nesting = less spaghetti code = good

## While Loops

The ability to repeat code can be extremely useful. While loops use a condition, just like if statements. 

```
int x = 0;
while (x < 4){
    System.out.println(x * 4);
    x++;   
}
```

that code will set x to zero and then only if x is less than 4: print x and increase x by one. Then it will go back up and repeat the check if x is less than 4. It will keep looping around until the check fails. The output will look like this:

```
0
4
8
12
```

You can easily make infinite loops. `true` is always `true` so the condition will always pass. 

```
while (true){
    calledInfiniteTimesLOL();
}
```

You can also force a loop to exit early by using the `break;` statement. This will immediately exit the loop and move on to the code in the next block. 

```
while (carHasGas){
    moveForward();
    if (wasBreakPushed){
        break;
    }
}
```

You can also skip the remaining part of a loop and immediately restart at the condition. 

```
while (true){
    doSomething();
    if (bar){
        continue;
    }
    somethingElse();
}
```

is equivalent to 

```
while (true){
    doSomething();
    if (!bar){
        somethingElse();
    }
}
```

## For Loops

There is a more efficient way to write my first while loop example. 

```
for (int x=0;x<4;x++){
    System.out.println(x * 4);
}
```

Instead of the first set of brackets just containing a condition, it has 3 statements. 
1. called at the beginning, the first time the loop runs. commonly to initialize a counter variable
2. the condition checked before each iteration. the loop ends if this is false
3. called at the end of each iteration. commonly to increment the counter variable

`break` and `continue` statements work the same as before. 

## Scopes 

Variables declared within {a code block} cannot be accessed from outside the block. They can however, be accessed by inner blocks.

```
int a = 0;
if (foo){
    // can access a 
    while (bar){
        float b = 2.7f;
        // do some math whatever idk
        // can access a and b
    }
    // can not access b anymore
}
```

---

# to be continued...

[Join the discord server](https://discord.gg/VbZVnRd) to be notified when more of this tutorial is released.

- Objects

- Methods

- Classes

- Inheritance

- Interfaces

- Exceptions
    - the most common exception is a NullPointerException

- Example Type: String
    - which holds an immutable sequence of characters like a word or a paragraph
- Example Type: ArrayList 
    - which holds a dynamic sequence of any type
    - compared to an array 
    - list interface 

- Example Type: HashMap
    - Maps keys to values 

    - Map interface 

- Example Type: Supplier
- Generics
