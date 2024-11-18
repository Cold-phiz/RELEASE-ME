# My Language

## Preq's:

- Purpose:
  
  - Designed for game design, applications and general purpose/backend programing

- Style: 
  
  - Custom concise style inspired by rust, python and lua

- Features:
  
  - To include dynamic typing, safety, speed, efficiency, and easy configurability 
  
  - Python and rust combined style of syntax
  
  - A standard library specifically for application and ui design (custimizable properties for everything like html and css)
  
  - Library for game development



## Syntax examples:

```My Language
// Comment

import library


// Variables

let variable_string = "value"
let variable_int = 1
let varibale_list = ["item1", "item2"]
let variable_tuple = ("item1", 2)
let variable_dict = {}

// No point in having const; if you don't want something to change
// don't change it.


// Functions

fn function_name(value_1 = 1, value_2 = 2) {
    value_1 += 1

    // Operators include: += -= = and . (to clear)
    
    return value_2 + value_1
}

function_name()     // Outputs 4
function_name(2, 2) // Outputs 5


// Conditionals

if (something > value) {
    print(string)
} else {
    print(other_string)
}

// I like how javascript does if statements, they look nice.


// Loops

for (something in something_else) {
    // do something
}

while (something == something_else) {
    // do soemthing_else
}

// Operations include: == =< => !=

// Copied the javascript conditionals and used them as loops.


// Classes

class my_class {
    fn init(value, other_value) {
        self.value = value
        self.other_value = other_value
    }

    fn fucntion() {
        return self.value + self.other_value
    }
}

let call = my_class(1, 2)
print(my_class.function())

// Pretty simple, like a mix of python and javascript


// Asynchronous Code (error handling)

try {
    some_function()
} except (error) {
    print("Error: ", error)
} finally {
    some_function_to_cleanup()
}

// Another mix of python and javascript
// Leave except without brackets if you don't want to use the
// error message associated with it. Finally is optional 
// (whatever's in the brackets is the variable name it is 
// stored in).


// Template Literals

let value = 1
let other_value = "Value: ${value + 1}"

// Same way javascript embeds variables


// Type Inference/Type annotations (optional)

let int(value) = 1
let string(value) = "text"

// Same as python if wanted, otherwise it's automatically inferred 
// depending on the first value given to the variable.


```


