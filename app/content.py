"""
Static content for the OOP dojo. Everything lives in code (not a DB) so it's
easy to read, diff, and extend - add a topic by adding a dict to a level's
`topics` list. Progress (what the learner has done) is the only thing that
lives in the database; see models.py.
"""

LEVELS = [
    {
        "id": "beginner",
        "name": "Beginner",
        "belt": "White Belt",
        "color": "#E8E6E1",
        "description": "The vocabulary of OOP: classes, objects, attributes, methods, and why we bother with any of it.",
        "topics": [
            {
                "id": "classes-and-objects",
                "title": "Classes & Objects",
                "tagline": "The blueprint and the thing built from it",
                "theory": """
A **class** is a blueprint. An **object** (or instance) is a specific thing built from that blueprint.
`class Dog:` describes what every dog can do and know; `Dog("Rex")` creates one actual dog named Rex.

Every method you define on a class automatically receives the instance as its first argument, `self`.
That's how `rex.bark()` knows *which* dog is barking - Python passes `rex` in as `self` behind the scenes.

The `__init__` method runs automatically when an object is created. It's not a "constructor" in the C++/Java
sense (the object already exists by the time `__init__` runs) - it's an *initializer* that sets up the
object's starting state.

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} says Woof!"

rex = Dog("Rex", "Labrador")
rex.bark()  # "Rex says Woof!"
```

Interview framing: when someone asks "what's the difference between a class and an object", the crisp
answer is *type vs instance* - a class defines the shape of data and behavior, an object is one concrete
value of that shape, living in memory with its own attribute values.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What does `self` refer to inside an instance method?",
                        "options": [
                            {"id": "a", "text": "The class itself"},
                            {"id": "b", "text": "The specific object the method was called on"},
                            {"id": "c", "text": "A reserved keyword with no real value"},
                            {"id": "d", "text": "The parent class"},
                        ],
                        "correct": "b",
                        "explanation": "`self` is just a strongly-conventional name for the first parameter, which Python automatically fills in with the instance the method was called on.",
                    },
                    {
                        "id": "q2",
                        "question": "What is the main job of `__init__`?",
                        "options": [
                            {"id": "a", "text": "It allocates memory for the object before it exists"},
                            {"id": "b", "text": "It sets up the initial state of an already-created object"},
                            {"id": "c", "text": "It deletes the object when it's no longer needed"},
                            {"id": "d", "text": "It converts the object to a string"},
                        ],
                        "correct": "b",
                        "explanation": "By the time `__init__` runs, the object already exists (created by `__new__`); `__init__` just initializes its attributes.",
                    },
                    {
                        "id": "q3",
                        "question": "Given `class Dog: pass` and `a = Dog(); b = Dog()`, what is `a == b`?",
                        "options": [
                            {"id": "a", "text": "True, because they're both Dog objects"},
                            {"id": "b", "text": "False, because they're different objects in memory with default identity-based equality"},
                            {"id": "c", "text": "A TypeError is raised"},
                            {"id": "d", "text": "True, because Python interns all objects"},
                        ],
                        "correct": "b",
                        "explanation": "Without a custom `__eq__`, `==` falls back to identity comparison (same as `is`) - two separate instances are never equal by default.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Write a `Book` class with `__init__(self, title, author, pages)` storing those three as attributes, and a method `summary(self)` that returns the string `'\"<title>\" by <author> (<pages> pages)'`.",
                    "starter_code": "class Book:\n    def __init__(self, title, author, pages):\n        # TODO\n        pass\n\n    def summary(self):\n        # TODO\n        pass\n",
                    "example": 'Book("Dune", "Frank Herbert", 412).summary() -> \'"Dune" by Frank Herbert (412 pages)\'',
                    "tests": [
                        {"name": "stores attributes", "code": "b = Book('Dune', 'Frank Herbert', 412)\nassert b.title == 'Dune' and b.author == 'Frank Herbert' and b.pages == 412"},
                        {"name": "summary format", "code": "b = Book('Dune', 'Frank Herbert', 412)\nassert b.summary() == '\"Dune\" by Frank Herbert (412 pages)'"},
                        {"name": "works for a second book", "code": "b = Book('1984', 'George Orwell', 328)\nassert b.summary() == '\"1984\" by George Orwell (328 pages)'"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "Explain the difference between a class and an instance to someone non-technical.",
                        "hint": "Reach for a real-world blueprint/template analogy.",
                        "model_answer": "A class is like a cookie cutter - it defines a shape. An instance is an actual cookie made from it. You can make many cookies (instances) from one cutter (class), and each cookie can be decorated differently (have different attribute values) while sharing the same basic shape (methods/structure).",
                    },
                    {
                        "id": "i2",
                        "question": "Why might a design have a class with zero instances ever created?",
                        "hint": "Think about namespacing, static utility methods, or abstract base classes.",
                        "model_answer": "A class can be used purely as a namespace for related static/class methods (e.g. a `MathUtils` class), or as an abstract base class that only exists to be subclassed and is never meant to be instantiated directly.",
                    },
                ],
            },
            {
                "id": "attributes-and-methods",
                "title": "Attributes & Methods",
                "tagline": "Instance vs class-level state and behavior",
                "theory": """
**Instance attributes** live on `self` and differ per object (`self.name`). **Class attributes** are
defined directly in the class body and are shared by every instance unless overridden:

```python
class Dog:
    species = "Canis familiaris"   # class attribute - shared

    def __init__(self, name):
        self.name = name           # instance attribute - per-object
```

There are three kinds of methods:
- **Instance methods** (`def bark(self)`) - operate on one object's state.
- **Class methods** (`@classmethod def from_string(cls, s)`) - operate on the class itself, often used as
  alternative constructors. They receive `cls`, not `self`.
- **Static methods** (`@staticmethod def is_valid_name(name)`) - live inside the class for organization but
  touch neither instance nor class state; they're really just plain functions grouped under a class.

A common interview trap: mutable default class attributes. If a class attribute is a list or dict, every
instance shares the *same* object unless you create it fresh in `__init__` - this causes bugs where
appending to one instance's "own" list mysteriously affects every other instance.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What decorator makes a method receive the class (`cls`) instead of the instance (`self`)?",
                        "options": [
                            {"id": "a", "text": "@staticmethod"},
                            {"id": "b", "text": "@property"},
                            {"id": "c", "text": "@classmethod"},
                            {"id": "d", "text": "@abstractmethod"},
                        ],
                        "correct": "c",
                        "explanation": "`@classmethod` binds the first parameter to the class itself (`cls`), commonly used for alternative constructors.",
                    },
                    {
                        "id": "q2",
                        "question": "class Counter:\n    items = []\n    def add(self, x):\n        self.items.append(x)\n\na, b = Counter(), Counter()\na.add(1)\nWhat is len(b.items)?",
                        "options": [
                            {"id": "a", "text": "0"},
                            {"id": "b", "text": "1"},
                            {"id": "c", "text": "A crash"},
                            {"id": "d", "text": "Undefined behavior"},
                        ],
                        "correct": "b",
                        "explanation": "`items` is a class attribute (a single shared list), so `a.add(1)` mutates the *one* list every instance points to - `b.items` sees it too. This is the classic mutable-class-attribute trap.",
                    },
                    {
                        "id": "q3",
                        "question": "When is a @staticmethod the right choice?",
                        "options": [
                            {"id": "a", "text": "When the method needs to read instance attributes"},
                            {"id": "b", "text": "When the method logically belongs to the class's namespace but needs neither self nor cls"},
                            {"id": "c", "text": "When you want to override it in a subclass based on instance state"},
                            {"id": "d", "text": "Never - always prefer instance methods"},
                        ],
                        "correct": "b",
                        "explanation": "Static methods are for utility functions that are conceptually related to the class but don't need any per-instance or per-class data.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Write a `BankAccount` class with a class attribute `bank_name = \"Dojo Bank\"`, an instance attribute `balance` starting at 0, a method `deposit(self, amount)` that adds to balance, and a classmethod `from_opening_balance(cls, amount)` that creates an account and immediately deposits `amount`.",
                    "starter_code": "class BankAccount:\n    bank_name = \"Dojo Bank\"\n\n    def __init__(self):\n        self.balance = 0\n\n    def deposit(self, amount):\n        # TODO\n        pass\n\n    @classmethod\n    def from_opening_balance(cls, amount):\n        # TODO: create an account and deposit `amount` into it, then return it\n        pass\n",
                    "example": "BankAccount.from_opening_balance(100).balance -> 100",
                    "tests": [
                        {"name": "deposit increases balance", "code": "a = BankAccount()\na.deposit(50)\nassert a.balance == 50"},
                        {"name": "class attribute shared", "code": "assert BankAccount.bank_name == 'Dojo Bank'"},
                        {"name": "alternative constructor", "code": "a = BankAccount.from_opening_balance(100)\nassert isinstance(a, BankAccount) and a.balance == 100"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "What bug can mutable class attributes cause, and how do you avoid it?",
                        "hint": "Think about lists/dicts defined directly in the class body.",
                        "model_answer": "Because a class attribute is one object shared by all instances, mutating it through one instance (e.g. `self.items.append(x)` where `items` is a class-level list) changes it for every instance. Fix it by initializing the attribute inside `__init__` (`self.items = []`) so each instance gets its own object.",
                    },
                    {
                        "id": "i2",
                        "question": "When would you reach for a classmethod as an 'alternative constructor' instead of just adding parameters to __init__?",
                        "hint": "Think about constructing an object from a different shape of input, like a CSV row or a JSON dict.",
                        "model_answer": "When there are multiple sensible ways to build an object from different input shapes (e.g. `Point.from_tuple(...)`, `Point.origin()`, `User.from_json(...)`), separate classmethods keep `__init__` simple and each constructor's intent explicit, instead of one `__init__` with a pile of optional/conflicting parameters.",
                    },
                ],
            },
            {
                "id": "encapsulation-basics",
                "title": "Encapsulation",
                "tagline": "Hiding internal state behind a clean interface",
                "theory": """
Encapsulation means bundling data with the methods that operate on it, and controlling access to that data
so outside code can't put an object into an invalid state.

Python doesn't have true private attributes, only conventions:
- `self.name` - public, anyone can read/write it.
- `self._name` - "protected" by convention: a signal to other developers that it's internal, but nothing
  stops access.
- `self.__name` - "name-mangled": Python rewrites it to `self._ClassName__name`, which makes accidental
  access from outside (or from a subclass) harder, though not impossible.

The idiomatic Python way to guard a value is `@property`:

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value
```

Callers still write `t.celsius = 20`, but now that assignment runs validation. This is the core interview
point: encapsulation isn't about "hiding for hiding's sake", it's about making invalid states unrepresentable
through the public interface.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What does a leading double underscore (`self.__x`) actually do in Python?",
                        "options": [
                            {"id": "a", "text": "Makes the attribute truly private and inaccessible"},
                            {"id": "b", "text": "Name-mangles it to _ClassName__x, making accidental access harder but not impossible"},
                            {"id": "c", "text": "Turns it into a class attribute"},
                            {"id": "d", "text": "Raises a SyntaxError"},
                        ],
                        "correct": "b",
                        "explanation": "Python has no enforced privacy. Double-underscore triggers name mangling, mainly to avoid naming clashes in subclasses, not to create real access control.",
                    },
                    {
                        "id": "q2",
                        "question": "What is the main benefit of using @property over a plain public attribute?",
                        "options": [
                            {"id": "a", "text": "Properties are faster than attribute access"},
                            {"id": "b", "text": "You can add validation/logic on get or set while keeping the same simple attribute-style syntax for callers"},
                            {"id": "c", "text": "Properties automatically serialize to JSON"},
                            {"id": "d", "text": "Properties can't be overridden in subclasses"},
                        ],
                        "correct": "b",
                        "explanation": "@property lets you start with a plain attribute and later add validation/computed logic without changing the calling code from `obj.x` to `obj.get_x()`.",
                    },
                    {
                        "id": "q3",
                        "question": "Which best describes the Python philosophy toward access control, often summarized as 'we're all consenting adults here'?",
                        "options": [
                            {"id": "a", "text": "Access control is enforced strictly by the interpreter, like Java's private keyword"},
                            {"id": "b", "text": "Python relies on naming conventions (_x, __x) and trusts developers not to poke at internals rather than hard-enforcing privacy"},
                            {"id": "c", "text": "Python has no concept of encapsulation at all"},
                            {"id": "d", "text": "All attributes must be accessed through getters and setters"},
                        ],
                        "correct": "b",
                        "explanation": "Python favors convention over enforcement - it trusts you, and gives you `@property` when you actually need to intercept access.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Write a `Temperature` class that stores Celsius internally, exposes a `celsius` property with a setter that raises `ValueError` if set below -273.15, and a read-only property `fahrenheit` computed from celsius.",
                    "starter_code": "class Temperature:\n    def __init__(self, celsius):\n        self._celsius = celsius\n\n    @property\n    def celsius(self):\n        # TODO\n        pass\n\n    @celsius.setter\n    def celsius(self, value):\n        # TODO: validate value >= -273.15, else raise ValueError\n        pass\n\n    @property\n    def fahrenheit(self):\n        # TODO: return celsius converted to fahrenheit\n        pass\n",
                    "example": "t = Temperature(0); t.fahrenheit -> 32.0",
                    "tests": [
                        {"name": "reads celsius", "code": "t = Temperature(20)\nassert t.celsius == 20"},
                        {"name": "fahrenheit conversion", "code": "t = Temperature(0)\nassert t.fahrenheit == 32.0"},
                        {"name": "rejects below absolute zero", "code": "t = Temperature(0)\ntry:\n    t.celsius = -300\n    assert False, 'expected ValueError'\nexcept ValueError:\n    pass"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "Why doesn't Python enforce private attributes the way Java does with `private`?",
                        "hint": "Think about Python's design philosophy around trust and flexibility.",
                        "model_answer": "Python favors convention and trust ('we're all consenting adults') over compiler-enforced access control. This keeps the language flexible (useful for debugging, testing, and metaprogramming) while still signaling intent through naming (`_x`, `__x`) and giving you `@property` when you need real gatekeeping.",
                    },
                    {
                        "id": "i2",
                        "question": "How would you refactor a class that started with a public attribute, once you discover you need validation on it, without breaking existing callers?",
                        "hint": "This is exactly the use case @property was designed for.",
                        "model_answer": "Rename the raw attribute to `_x`, then add an `@property` getter and setter named `x`. Callers who already write `obj.x` and `obj.x = value` keep working unchanged, but the setter can now validate.",
                    },
                ],
            },
        ],
    },
    {
        "id": "intermediate",
        "name": "Intermediate",
        "belt": "Yellow Belt",
        "color": "#E8C547",
        "description": "The pillars that make OOP powerful: inheritance, polymorphism, and abstraction.",
        "topics": [
            {
                "id": "inheritance",
                "title": "Inheritance",
                "tagline": "Reusing and specializing behavior",
                "theory": """
Inheritance lets a class (the subclass) reuse and extend behavior from another class (the superclass).

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} barks"
```

`Dog` inherits `__init__` from `Animal` for free, and *overrides* `speak`. Inside an override, `super()`
lets you call the parent's version instead of fully replacing it:

```python
class Dog(Animal):
    def speak(self):
        base = super().speak()
        return f"{base}, specifically a bark"
```

Python supports **multiple inheritance** (`class C(A, B)`), resolved via the Method Resolution Order (MRO,
computed with the C3 linearization algorithm) - you can inspect it with `C.__mro__`.

Interview-critical distinction: inheritance models an **"is-a"** relationship (a Dog *is an* Animal). If the
relationship is really **"has-a"** (a Car *has an* Engine), that's composition, not inheritance - a very
common design-question trap (see the Composition vs Inheritance topic in Advanced).
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What does `super().__init__(...)` do inside a subclass's `__init__`?",
                        "options": [
                            {"id": "a", "text": "Creates a brand new, separate instance of the parent class"},
                            {"id": "b", "text": "Calls the parent class's __init__ on the current instance, so it can set up its part of the state"},
                            {"id": "c", "text": "Deletes the subclass's own __init__"},
                            {"id": "d", "text": "Is only valid in single inheritance, never multiple inheritance"},
                        ],
                        "correct": "b",
                        "explanation": "`super()` gives you a proxy to the next class in the MRO, letting you extend rather than fully replace inherited behavior.",
                    },
                    {
                        "id": "q2",
                        "question": "What determines which class's method runs when multiple parent classes define the same method name?",
                        "options": [
                            {"id": "a", "text": "Alphabetical order of class names"},
                            {"id": "b", "text": "The Method Resolution Order (MRO), computed via C3 linearization"},
                            {"id": "c", "text": "Whichever parent was defined most recently in the file"},
                            {"id": "d", "text": "Python raises an error instead of choosing"},
                        ],
                        "correct": "b",
                        "explanation": "Python computes a deterministic MRO for every class; you can inspect it with `ClassName.__mro__` or `ClassName.mro()`.",
                    },
                    {
                        "id": "q3",
                        "question": "Which relationship is inheritance best suited to model?",
                        "options": [
                            {"id": "a", "text": "\"has-a\", e.g. a Car has an Engine"},
                            {"id": "b", "text": "\"is-a\", e.g. a Dog is an Animal"},
                            {"id": "c", "text": "\"uses-a\", e.g. a function uses a logger"},
                            {"id": "d", "text": "No particular relationship - it's purely for code reuse"},
                        ],
                        "correct": "b",
                        "explanation": "Inheritance should model true is-a relationships. Reusing code between unrelated things via inheritance is a classic anti-pattern; composition is usually the better tool for has-a/uses-a.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Write a base `Shape` class with a method `area(self)` that raises `NotImplementedError`, and two subclasses `Rectangle(width, height)` and `Circle(radius)` that each override `area()` correctly (use `3.14159` for pi).",
                    "starter_code": "class Shape:\n    def area(self):\n        raise NotImplementedError\n\nclass Rectangle(Shape):\n    def __init__(self, width, height):\n        # TODO\n        pass\n\n    def area(self):\n        # TODO\n        pass\n\nclass Circle(Shape):\n    def __init__(self, radius):\n        # TODO\n        pass\n\n    def area(self):\n        # TODO: use 3.14159 for pi\n        pass\n",
                    "example": "Rectangle(3, 4).area() -> 12",
                    "tests": [
                        {"name": "rectangle area", "code": "assert Rectangle(3, 4).area() == 12"},
                        {"name": "circle area", "code": "assert abs(Circle(2).area() - 12.56636) < 1e-6"},
                        {"name": "both are Shapes", "code": "assert isinstance(Rectangle(1,1), Shape) and isinstance(Circle(1), Shape)"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "What's the difference between overriding a method and overloading a method? Does Python support both?",
                        "hint": "Think about what each term means in languages like Java, and how Python differs.",
                        "model_answer": "Overriding means a subclass redefines a method it inherited, changing behavior for that subclass - Python fully supports this. Overloading means having multiple methods with the same name but different parameter signatures, resolved at compile time - Python doesn't support this natively (a later `def` with the same name just replaces the earlier one); the usual workaround is default arguments, `*args`/`**kwargs`, or `functools.singledispatch`.",
                    },
                    {
                        "id": "i2",
                        "question": "Why is deep multiple inheritance often considered risky in real codebases?",
                        "hint": "Think about the 'diamond problem' and how easy the resulting MRO is to reason about.",
                        "model_answer": "Deep or wide multiple inheritance makes the MRO hard to reason about (the 'diamond problem'), makes it unclear which parent's method actually executes, and tightly couples unrelated hierarchies. Most style guides favor composition or mixins with a single, shallow inheritance chain instead.",
                    },
                ],
            },
            {
                "id": "polymorphism",
                "title": "Polymorphism",
                "tagline": "One interface, many implementations",
                "theory": """
Polymorphism means code can work with objects of different types through a shared interface, without
knowing (or caring) about their concrete class.

```python
shapes = [Rectangle(3, 4), Circle(2)]
for s in shapes:
    print(s.area())   # works for both, no type-checking required
```

This is **duck typing**: "if it walks like a duck and quacks like a duck, treat it like a duck." Python
doesn't require a shared base class for this to work - any object with an `.area()` method fits, because
Python checks capability, not declared type.

Operator overloading is polymorphism at the language level: defining `__add__` lets `+` work meaningfully
for your own classes:

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
```

Interview-critical distinction: **duck typing** (works because it has the right methods) vs
**structural typing checked by tools** (e.g. `typing.Protocol`) vs **nominal typing** (works because it
explicitly inherits from/declares an interface, like Java's `implements`). Python leans duck-typed at
runtime but supports the other two for static analysis.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What is 'duck typing'?",
                        "options": [
                            {"id": "a", "text": "A type system that requires explicit interface declarations"},
                            {"id": "b", "text": "Treating an object as usable based on the methods/attributes it has, not its declared class"},
                            {"id": "c", "text": "A Python-specific syntax for type hints"},
                            {"id": "d", "text": "A bug where types are inferred incorrectly"},
                        ],
                        "correct": "b",
                        "explanation": "\"If it walks like a duck and quacks like a duck...\" - Python cares whether the object supports the needed operation, not what class it's declared as.",
                    },
                    {
                        "id": "q2",
                        "question": "Which dunder method would you implement to make the `+` operator work between two instances of your class?",
                        "options": [
                            {"id": "a", "text": "__plus__"},
                            {"id": "b", "text": "__sum__"},
                            {"id": "c", "text": "__add__"},
                            {"id": "d", "text": "__combine__"},
                        ],
                        "correct": "c",
                        "explanation": "`__add__(self, other)` is invoked for `self + other`. There's also `__radd__` for when your object is on the right side of a `+` with an incompatible left operand.",
                    },
                    {
                        "id": "q3",
                        "question": "You have a list of different shape objects and call `.area()` on each in a loop without checking their type. What OOP principle is this an example of?",
                        "options": [
                            {"id": "a", "text": "Encapsulation"},
                            {"id": "b", "text": "Polymorphism"},
                            {"id": "c", "text": "Multiple inheritance"},
                            {"id": "d", "text": "Composition"},
                        ],
                        "correct": "b",
                        "explanation": "Calling the same method name and getting type-appropriate behavior back, without branching on type, is the definition of polymorphism.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Write a `Vector` class with `x, y` attributes, `__add__` (returns a new Vector), `__eq__` (compares x and y), and `__repr__` returning `'Vector(x, y)'`.",
                    "starter_code": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __add__(self, other):\n        # TODO\n        pass\n\n    def __eq__(self, other):\n        # TODO\n        pass\n\n    def __repr__(self):\n        # TODO\n        pass\n",
                    "example": "Vector(1, 2) + Vector(3, 4) -> Vector(4, 6)",
                    "tests": [
                        {"name": "addition", "code": "assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)"},
                        {"name": "equality", "code": "assert Vector(1, 1) == Vector(1, 1)\nassert not (Vector(1, 1) == Vector(2, 1))"},
                        {"name": "repr", "code": "assert repr(Vector(4, 6)) == 'Vector(4, 6)'"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "How does Python's duck typing differ from polymorphism via inheritance in Java/C#?",
                        "hint": "Think about whether a shared base class/interface is required.",
                        "model_answer": "In Java/C#, polymorphism typically requires the object's class to formally implement an interface or extend a base class, checked at compile time. Python doesn't require that relationship at all - any object that happens to have the right method (`.area()`, `.__len__()`, etc.) works, checked only at call time. This is more flexible but pushes type errors to runtime instead of compile time.",
                    },
                    {
                        "id": "i2",
                        "question": "Why should __eq__ and __hash__ usually be defined together?",
                        "hint": "Think about what happens if you put an object with a custom __eq__ into a set or dict.",
                        "model_answer": "Objects that compare equal should hash the same, or they'll break in sets/dicts (two 'equal' objects could land in different hash buckets and both be treated as present). Defining `__eq__` without `__hash__` actually makes the class unhashable by default in Python, since Python sets `__hash__` to `None` automatically when you override `__eq__`.",
                    },
                ],
            },
            {
                "id": "abstraction-abc",
                "title": "Abstraction & ABCs",
                "tagline": "Defining a contract without an implementation",
                "theory": """
Abstraction means exposing *what* something does while hiding *how*. In Python this is formalized with
**Abstract Base Classes** (`abc` module):

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        ...

class CreditCard(PaymentMethod):
    def pay(self, amount):
        return f"Charged ${amount} to credit card"
```

`PaymentMethod` can never be instantiated directly (`PaymentMethod()` raises `TypeError`). Any subclass
*must* implement `pay`, or it also can't be instantiated - Python enforces the contract at instantiation
time.

This is different from just raising `NotImplementedError` in a plain base class: that only fails at
*call* time, if someone forgets to override it and then calls the method. `ABC` + `@abstractmethod` fails
at *instantiation* time, catching the mistake much earlier - a real advantage in interviews when comparing
the two approaches.

Abstraction is closely related to Java/C#'s formal **interfaces**: a fully abstract class with only
abstract methods and no shared implementation is effectively an interface.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What happens if you try to instantiate an ABC that still has an unimplemented @abstractmethod?",
                        "options": [
                            {"id": "a", "text": "It works, but calling the abstract method raises an error"},
                            {"id": "b", "text": "Python raises a TypeError at instantiation time"},
                            {"id": "c", "text": "It silently creates an incomplete object"},
                            {"id": "d", "text": "A SyntaxError is raised when the class is defined"},
                        ],
                        "correct": "b",
                        "explanation": "ABC + abstractmethod enforces the contract as early as possible: you can't even create the object until every abstract method is implemented.",
                    },
                    {
                        "id": "q2",
                        "question": "How does using ABC + @abstractmethod differ from just raising NotImplementedError in a base class method?",
                        "options": [
                            {"id": "a", "text": "There's no real difference"},
                            {"id": "b", "text": "NotImplementedError only fails when the method is called; ABC fails as soon as you try to instantiate an incomplete subclass"},
                            {"id": "c", "text": "ABC is slower at runtime"},
                            {"id": "d", "text": "NotImplementedError can only be used with multiple inheritance"},
                        ],
                        "correct": "b",
                        "explanation": "This is the key practical distinction, and a great thing to bring up unprompted in an interview - ABCs shift the error earlier, which is generally better.",
                    },
                    {
                        "id": "q3",
                        "question": "What best describes the relationship between 'abstraction' and 'encapsulation'?",
                        "options": [
                            {"id": "a", "text": "They're the same thing"},
                            {"id": "b", "text": "Abstraction hides complexity by exposing only a simplified interface (what); encapsulation hides internal state/data (how it's protected)"},
                            {"id": "c", "text": "Abstraction only applies to functions, encapsulation only to classes"},
                            {"id": "d", "text": "Encapsulation is a subtype of inheritance"},
                        ],
                        "correct": "b",
                        "explanation": "They're closely related but distinct: abstraction is about interface design (what callers see), encapsulation is about protecting internal state (how it's guarded). Confusing these two is one of the most common interview stumbles.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Using `abc.ABC` and `@abstractmethod`, write an abstract `Notifier` class with an abstract method `send(self, message)`. Then write `EmailNotifier` and `SMSNotifier` subclasses whose `send` returns `'Email: <message>'` and `'SMS: <message>'` respectively.",
                    "starter_code": "from abc import ABC, abstractmethod\n\nclass Notifier(ABC):\n    @abstractmethod\n    def send(self, message):\n        ...\n\nclass EmailNotifier(Notifier):\n    def send(self, message):\n        # TODO\n        pass\n\nclass SMSNotifier(Notifier):\n    def send(self, message):\n        # TODO\n        pass\n",
                    "example": "EmailNotifier().send('hi') -> 'Email: hi'",
                    "tests": [
                        {"name": "email format", "code": "assert EmailNotifier().send('hi') == 'Email: hi'"},
                        {"name": "sms format", "code": "assert SMSNotifier().send('hi') == 'SMS: hi'"},
                        {"name": "abstract class cannot be instantiated", "code": "try:\n    Notifier()\n    assert False, 'expected TypeError'\nexcept TypeError:\n    pass"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "When would you choose an ABC over a plain base class with NotImplementedError, and when might the plain version actually be fine?",
                        "hint": "Consider team size, how strict the contract needs to be, and whether it's a quick internal script vs a shared library.",
                        "model_answer": "Use an ABC when the contract matters - a shared library or multi-person codebase where you want to fail fast if a subclass is incomplete. A plain NotImplementedError base class is fine for a small script or prototype where the extra ceremony isn't worth it and the 'contract' is really just documentation.",
                    },
                    {
                        "id": "i2",
                        "question": "How do Python's ABCs compare to Java interfaces?",
                        "hint": "Think about multiple inheritance and default implementations.",
                        "model_answer": "Both define a contract that implementers must satisfy. Python's ABCs can mix in real implemented methods alongside abstract ones (like Java's default methods), and Python supports multiple inheritance directly, so a class can inherit from several ABCs at once, similar to implementing multiple interfaces in Java.",
                    },
                ],
            },
        ],
    },
    {
        "id": "advanced",
        "name": "Advanced",
        "belt": "Blue Belt",
        "color": "#4A90E2",
        "description": "Where OOP theory meets real design decisions: operator overloading, composition, and SOLID.",
        "topics": [
            {
                "id": "dunder-methods",
                "title": "Dunder Methods",
                "tagline": "Making your objects behave like built-ins",
                "theory": """
"Dunder" (double-underscore) methods are how Python objects hook into language-level syntax and built-in
functions. A few of the most important ones:

- `__repr__` - unambiguous developer-facing representation (`repr(obj)`, shown in the REPL/debugger).
- `__str__` - human-friendly representation (`str(obj)`, used by `print()`). Falls back to `__repr__` if
  not defined.
- `__eq__`, `__lt__`, etc. - comparison operators (`==`, `<`, ...). Note `__lt__` alone doesn't give you
  `>`; use `functools.total_ordering` to fill in the rest from a couple of them.
- `__len__` - powers `len(obj)`.
- `__getitem__` / `__setitem__` - powers `obj[key]` and `obj[key] = value`, and makes the object iterable
  by index even without `__iter__`.
- `__iter__` / `__next__` - makes an object a proper iterator, usable in `for x in obj`.
- `__enter__` / `__exit__` - makes an object usable as a context manager, i.e. `with obj:`.

This is called **operator overloading**, and it's the mechanism behind Python's whole philosophy of
"everything is an object with a well-defined protocol" - a `list`, a `dict`, and your own custom class can
all be used with `len()`, `for`, `[]`, etc. as long as they implement the right dunders.

A common good practice: always implement `__repr__` (it makes debugging dramatically easier), and only add
`__str__` if you want a different, prettier user-facing format.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What's the key difference between __str__ and __repr__?",
                        "options": [
                            {"id": "a", "text": "They're identical, just different names"},
                            {"id": "b", "text": "__repr__ is meant to be unambiguous for developers/debugging; __str__ is a friendlier user-facing format, and falls back to __repr__ if missing"},
                            {"id": "c", "text": "__str__ is required, __repr__ is optional"},
                            {"id": "d", "text": "__repr__ only works on numbers"},
                        ],
                        "correct": "b",
                        "explanation": "A good rule of thumb: __repr__(obj) should ideally look like valid Python that could recreate the object, e.g. `Point(x=1, y=2)`.",
                    },
                    {
                        "id": "q2",
                        "question": "Which dunder method(s) are required to make an object usable in a `with obj:` block?",
                        "options": [
                            {"id": "a", "text": "__enter__ and __exit__"},
                            {"id": "b", "text": "__iter__ and __next__"},
                            {"id": "c", "text": "__len__ only"},
                            {"id": "d", "text": "__context__ and __manage__"},
                        ],
                        "correct": "a",
                        "explanation": "__enter__ runs at the start of the `with` block and its return value is bound by `as`; __exit__ runs at the end (even on exception) and can suppress exceptions by returning True.",
                    },
                    {
                        "id": "q3",
                        "question": "If you define __eq__ but not __hash__, what happens to instances of that class?",
                        "options": [
                            {"id": "a", "text": "Nothing changes, __hash__ is unaffected"},
                            {"id": "b", "text": "Python automatically sets __hash__ to None, making instances unhashable (can't go in a set or be a dict key)"},
                            {"id": "c", "text": "Python raises an error immediately when the class is defined"},
                            {"id": "d", "text": "__hash__ is generated automatically from __eq__'s logic"},
                        ],
                        "correct": "b",
                        "explanation": "This trips people up constantly - defining __eq__ silently makes your objects unhashable unless you also define __hash__ (or explicitly set it to inherit from object).",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Write a `Deck` class wrapping a list of card strings (`self.cards`) that supports `len(deck)` via `__len__`, `deck[i]` via `__getitem__`, and iteration via `__iter__` (returning `iter(self.cards)`).",
                    "starter_code": "class Deck:\n    def __init__(self, cards):\n        self.cards = cards\n\n    def __len__(self):\n        # TODO\n        pass\n\n    def __getitem__(self, index):\n        # TODO\n        pass\n\n    def __iter__(self):\n        # TODO\n        pass\n",
                    "example": "len(Deck(['A', 'K', 'Q'])) -> 3",
                    "tests": [
                        {"name": "len works", "code": "assert len(Deck(['A', 'K', 'Q'])) == 3"},
                        {"name": "indexing works", "code": "d = Deck(['A', 'K', 'Q'])\nassert d[0] == 'A' and d[2] == 'Q'"},
                        {"name": "iteration works", "code": "d = Deck(['A', 'K', 'Q'])\nassert list(d) == ['A', 'K', 'Q']"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "Why does Python favor 'protocols' (dunder methods) over requiring explicit interfaces for things like iteration or length?",
                        "hint": "Think back to duck typing.",
                        "model_answer": "It's duck typing applied at the language level: `len()`, `for`, `[]`, etc. work on *any* object that implements the right dunder, regardless of its class hierarchy. This lets built-in types and user classes interoperate through shared protocols instead of requiring everything to inherit from a common base.",
                    },
                    {
                        "id": "i2",
                        "question": "If you only implement __getitem__ (not __iter__), can you still do `for x in obj`? Why?",
                        "hint": "Python has an old-style iteration fallback for sequences.",
                        "model_answer": "Yes - if `__iter__` is missing, Python falls back to calling `__getitem__` with increasing integer indices (0, 1, 2, ...) until it raises `IndexError`. This is a legacy protocol kept for backward compatibility, but explicitly defining `__iter__` is clearer and preferred in modern code.",
                    },
                ],
            },
            {
                "id": "composition-vs-inheritance",
                "title": "Composition vs Inheritance",
                "tagline": "\"Favor composition over inheritance\"",
                "theory": """
**Composition** builds objects out of other objects (a "has-a" relationship), instead of extending a base
class (an "is-a" relationship):

```python
class Engine:
    def start(self):
        return "Engine starting"

class Car:
    def __init__(self):
        self.engine = Engine()   # Car HAS AN Engine

    def start(self):
        return self.engine.start()
```

Why prefer composition in many cases? Inheritance creates **tight coupling**: a subclass depends on its
parent's implementation details, and changes to the parent can silently break subclasses (the "fragile
base class" problem). Deep inheritance hierarchies also become hard to reason about and hard to change.

Composition is more flexible: you can swap the `Engine` for an `ElectricEngine` at runtime, combine
several small, focused objects, and avoid forcing an artificial "is-a" relationship where it doesn't
really exist (e.g. modeling `ElectricCar` as inheriting from `GasCar` just to reuse code, when it isn't
really a gas car at all).

This is the "favor composition over inheritance" principle from the Gang of Four design patterns book -
one of the most quoted lines in OOP interviews. The practical test: ask "is a Car an Engine?" (no - so
don't inherit) vs "does a Car have an Engine?" (yes - so compose).
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What problem does 'favor composition over inheritance' mainly try to avoid?",
                        "options": [
                            {"id": "a", "text": "Slow runtime performance"},
                            {"id": "b", "text": "Tight coupling and fragile base classes, where changing a parent silently breaks subclasses"},
                            {"id": "c", "text": "Python's inability to support inheritance well"},
                            {"id": "d", "text": "Memory leaks"},
                        ],
                        "correct": "b",
                        "explanation": "Inheritance ties a subclass's correctness to implementation details of its parent, which is exactly what composition avoids by using clean, swappable interfaces instead.",
                    },
                    {
                        "id": "q2",
                        "question": "A `Car` needs an `Engine`. Which relationship is this, and which technique fits?",
                        "options": [
                            {"id": "a", "text": "\"is-a\", use inheritance: class Car(Engine)"},
                            {"id": "b", "text": "\"has-a\", use composition: self.engine = Engine()"},
                            {"id": "c", "text": "Neither applies, this needs multiple inheritance"},
                            {"id": "d", "text": "\"uses-a\", so no OOP technique is appropriate"},
                        ],
                        "correct": "b",
                        "explanation": "A Car is not a kind of Engine - it contains/uses one. That's a textbook has-a relationship, best modeled with composition.",
                    },
                    {
                        "id": "q3",
                        "question": "What's a concrete advantage composition has over inheritance for testing?",
                        "options": [
                            {"id": "a", "text": "None, they're equivalent for testing"},
                            {"id": "b", "text": "You can inject a mock/fake dependency (e.g. a fake Engine) instead of the real one, since it's just an object reference"},
                            {"id": "c", "text": "Composition automatically generates unit tests"},
                            {"id": "d", "text": "Inheritance always makes mocking easier"},
                        ],
                        "correct": "b",
                        "explanation": "Because a composed dependency is just an attribute, you can swap in a test double at construction time (dependency injection) - much harder to do cleanly with inherited behavior.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Write an `Engine` class with a `start(self)` method returning `'Engine started'`, and a `Car` class that takes an `engine` object in `__init__` and has a `start(self)` method that returns `f'Car ready: {self.engine.start()}'`. This demonstrates composition and dependency injection (any object with a `.start()` method should work, not just `Engine`).",
                    "starter_code": "class Engine:\n    def start(self):\n        return 'Engine started'\n\nclass Car:\n    def __init__(self, engine):\n        # TODO: store the engine\n        pass\n\n    def start(self):\n        # TODO\n        pass\n",
                    "example": "Car(Engine()).start() -> 'Car ready: Engine started'",
                    "tests": [
                        {"name": "uses composed engine", "code": "assert Car(Engine()).start() == 'Car ready: Engine started'"},
                        {"name": "works with any object exposing start()", "code": "class FakeEngine:\n    def start(self):\n        return 'fake started'\nassert Car(FakeEngine()).start() == 'Car ready: fake started'"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "Give a real example where you'd catch yourself reaching for inheritance and then realize composition is the better fit.",
                        "hint": "Look for cases where you'd be inheriting just to reuse a method, not because of a true is-a relationship.",
                        "model_answer": "A common one: making a `Logger` mixin that many unrelated classes inherit from just to get a `.log()` method. None of those classes 'is-a' Logger - they just want logging *capability*. Composition (`self.logger = Logger()`, or even simpler, passing a logger in) models this correctly without forcing a fake hierarchy.",
                    },
                    {
                        "id": "i2",
                        "question": "Does 'favor composition over inheritance' mean you should never use inheritance? How do you decide?",
                        "hint": "Think about when the is-a relationship is genuinely true and stable.",
                        "model_answer": "No - it's a default bias, not an absolute rule. Inheritance is still the right tool when the is-a relationship is real, stable, and the subclass genuinely needs to be substitutable for the parent (Liskov substitution). The test is asking honestly: 'is X truly a kind of Y, in every context Y is used?' If yes, inheritance is fine; if you're on the fence, composition is usually the safer default.",
                    },
                ],
            },
            {
                "id": "solid-principles",
                "title": "SOLID Principles",
                "tagline": "Five rules for OOP code that survives change",
                "theory": """
SOLID is five design principles, and one of the most common things asked about directly in interviews:

**S - Single Responsibility Principle**: a class should have one reason to change. A `Report` class that
both calculates data *and* formats it as PDF *and* emails it has three reasons to change - split it up.

**O - Open/Closed Principle**: classes should be open for extension, closed for modification. Instead of
adding `if isinstance(shape, Circle): ... elif isinstance(shape, Square): ...` every time you add a shape,
design so new shapes can be added by writing a new subclass, without touching existing code.

**L - Liskov Substitution Principle**: a subclass should be usable anywhere its parent is expected, without
breaking correctness. Classic violation: `Square` inheriting from `Rectangle` and overriding `set_width` to
also change height - it breaks code that assumes setting a Rectangle's width leaves height alone.

**I - Interface Segregation Principle**: prefer several small, focused interfaces over one large one.
Don't force a class to implement methods it doesn't need just because they're bundled in one fat interface.

**D - Dependency Inversion Principle**: depend on abstractions, not concrete implementations. A
`NotificationService` should depend on an abstract `Notifier` interface, not directly on `EmailNotifier`,
so you can swap in `SMSNotifier` without changing `NotificationService`.

Interviewers love SOLID because each letter maps to a very concrete, common real-world code smell - being
able to name the smell *and* the fix is what separates "I've heard of SOLID" from "I use SOLID."
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "A `User` class both validates email format AND saves the user to the database. Which SOLID principle does this most directly violate?",
                        "options": [
                            {"id": "a", "text": "Liskov Substitution"},
                            {"id": "b", "text": "Single Responsibility"},
                            {"id": "c", "text": "Interface Segregation"},
                            {"id": "d", "text": "Dependency Inversion"},
                        ],
                        "correct": "b",
                        "explanation": "Validation logic and persistence logic are two different reasons to change - they should live in separate classes (e.g. a validator and a repository).",
                    },
                    {
                        "id": "q2",
                        "question": "The classic 'Square inherits from Rectangle, but overriding set_width also changes height' problem is the textbook violation of which principle?",
                        "options": [
                            {"id": "a", "text": "Open/Closed"},
                            {"id": "b", "text": "Liskov Substitution"},
                            {"id": "c", "text": "Interface Segregation"},
                            {"id": "d", "text": "Single Responsibility"},
                        ],
                        "correct": "b",
                        "explanation": "Code written against Rectangle (assuming width and height are independent) breaks when handed a Square - the subclass isn't truly substitutable for the parent.",
                    },
                    {
                        "id": "q3",
                        "question": "A `PaymentProcessor` class directly instantiates and depends on a concrete `StripeGateway` class inside its methods. What does Dependency Inversion suggest instead?",
                        "options": [
                            {"id": "a", "text": "PaymentProcessor should depend on an abstract Gateway interface, with StripeGateway (or others) injected in"},
                            {"id": "b", "text": "PaymentProcessor should inherit from StripeGateway"},
                            {"id": "c", "text": "There is no issue - this is fine as-is"},
                            {"id": "d", "text": "StripeGateway should be made a global singleton"},
                        ],
                        "correct": "a",
                        "explanation": "Depending on a concrete class means swapping payment providers requires modifying PaymentProcessor. Depending on an abstraction (interface/ABC) and injecting the concrete implementation decouples the two.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Apply Dependency Inversion: write an abstract `Storage` ABC with `save(self, data)`, a concrete `InMemoryStorage` implementing it (append `data` to a list `self.items`), and a `Repository` class whose `__init__(self, storage)` stores the injected storage, with a method `save_item(self, data)` that delegates to `storage.save(data)`.",
                    "starter_code": "from abc import ABC, abstractmethod\n\nclass Storage(ABC):\n    @abstractmethod\n    def save(self, data):\n        ...\n\nclass InMemoryStorage(Storage):\n    def __init__(self):\n        self.items = []\n\n    def save(self, data):\n        # TODO\n        pass\n\nclass Repository:\n    def __init__(self, storage):\n        # TODO\n        pass\n\n    def save_item(self, data):\n        # TODO: delegate to the injected storage\n        pass\n",
                    "example": "r = Repository(InMemoryStorage()); r.save_item('x'); r.storage.items -> ['x']",
                    "tests": [
                        {"name": "saves through injected storage", "code": "s = InMemoryStorage()\nr = Repository(s)\nr.save_item('x')\nassert s.items == ['x']"},
                        {"name": "repository has no hardcoded storage type", "code": "class OtherStorage(Storage):\n    def __init__(self):\n        self.items = []\n    def save(self, data):\n        self.items.append(data.upper())\ns = OtherStorage()\nr = Repository(s)\nr.save_item('x')\nassert s.items == ['X']"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "Walk through all five SOLID letters from memory, each with a one-line definition.",
                        "hint": "S-O-L-I-D. Say each principle out loud before checking.",
                        "model_answer": "S: Single Responsibility - a class should have one reason to change. O: Open/Closed - open for extension, closed for modification. L: Liskov Substitution - subclasses must be usable wherever their parent is expected. I: Interface Segregation - prefer small, focused interfaces over one large one. D: Dependency Inversion - depend on abstractions, not concrete implementations.",
                    },
                    {
                        "id": "i2",
                        "question": "Can following SOLID too rigidly ever hurt a codebase? What's the trade-off?",
                        "hint": "Think about over-engineering, extra abstraction layers, and YAGNI.",
                        "model_answer": "Yes - applying SOLID (especially D and I) too early can create excessive abstraction layers, interfaces with only one implementation, and indirection that makes simple code harder to follow. The pragmatic approach is to apply SOLID where real change/extension is expected or already happening, not preemptively on every class - this is the tension with YAGNI ('you aren't gonna need it').",
                    },
                ],
            },
        ],
    },
    {
        "id": "expert",
        "name": "Expert",
        "belt": "Black Belt",
        "color": "#D4AF37",
        "description": "Design patterns, the metaclass/MRO machinery under the hood, and full system-design-style OOP interviews.",
        "topics": [
            {
                "id": "design-patterns",
                "title": "Design Patterns",
                "tagline": "Named solutions to recurring design problems",
                "theory": """
Design patterns are reusable solutions to problems that show up again and again in OOP design. You don't
need to memorize all 23 Gang-of-Four patterns, but a handful come up constantly in interviews:

**Singleton** - ensure a class has only one instance, with a global access point. Often *overused* in
practice (it's really just global state), but useful for things like a single shared config or connection
pool.

**Factory** - a method/class whose job is to create objects, so calling code doesn't need to know the exact
class being instantiated:
```python
def create_notifier(kind):
    return {"email": EmailNotifier, "sms": SMSNotifier}[kind]()
```

**Strategy** - encapsulate interchangeable algorithms behind a common interface, and swap them at runtime:
```python
class Sorter:
    def __init__(self, strategy):
        self.strategy = strategy
    def sort(self, data):
        return self.strategy(data)
```
This is composition applied deliberately to make *behavior* pluggable.

**Observer** - objects (observers) subscribe to another object (subject) and get notified automatically on
state changes - the pattern behind most event/pub-sub systems and GUI callbacks.

**Decorator** - wrap an object to add behavior without modifying its class (Python's `@decorator` syntax
for functions is a direct application of this idea to functions rather than objects).

Interview framing: patterns aren't a checklist to force into every answer - the strong move is naming the
*problem* a pattern solves and only reaching for it when that specific problem shows up.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What core problem does the Strategy pattern solve?",
                        "options": [
                            {"id": "a", "text": "Ensuring only one instance of a class exists"},
                            {"id": "b", "text": "Making an algorithm/behavior swappable at runtime behind a common interface"},
                            {"id": "c", "text": "Notifying subscribers automatically when state changes"},
                            {"id": "d", "text": "Creating objects without specifying their exact class"},
                        ],
                        "correct": "b",
                        "explanation": "Strategy is composition applied to behavior: different interchangeable implementations of 'the algorithm' are plugged in behind one interface.",
                    },
                    {
                        "id": "q2",
                        "question": "A UI needs multiple widgets to update automatically whenever a shared data model changes, without the model knowing about the widgets in advance. Which pattern fits?",
                        "options": [
                            {"id": "a", "text": "Singleton"},
                            {"id": "b", "text": "Factory"},
                            {"id": "c", "text": "Observer"},
                            {"id": "d", "text": "Decorator"},
                        ],
                        "correct": "c",
                        "explanation": "Observer is exactly this: subjects notify a list of subscribed observers on state change, without needing to know their concrete types ahead of time.",
                    },
                    {
                        "id": "q3",
                        "question": "What is a commonly cited downside of overusing the Singleton pattern?",
                        "options": [
                            {"id": "a", "text": "It makes objects immutable"},
                            {"id": "b", "text": "It introduces hidden global state, making code harder to test and reason about"},
                            {"id": "c", "text": "It requires multiple inheritance"},
                            {"id": "d", "text": "Python doesn't support it at all"},
                        ],
                        "correct": "b",
                        "explanation": "A Singleton is effectively global mutable state with extra ceremony - it can make unit testing hard (state leaks between tests) and hides dependencies that would otherwise be explicit.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Implement the Strategy pattern: write a `Discount` interface-style base class with `apply(self, price)`, two strategies `NoDiscount` (returns price unchanged) and `PercentOff(percent)` (reduces price by that percent), and a `Cart` class taking a `discount` strategy in `__init__` with a method `checkout(self, price)` that delegates to it.",
                    "starter_code": "class Discount:\n    def apply(self, price):\n        raise NotImplementedError\n\nclass NoDiscount(Discount):\n    def apply(self, price):\n        # TODO\n        pass\n\nclass PercentOff(Discount):\n    def __init__(self, percent):\n        self.percent = percent\n\n    def apply(self, price):\n        # TODO: reduce price by self.percent percent\n        pass\n\nclass Cart:\n    def __init__(self, discount):\n        # TODO\n        pass\n\n    def checkout(self, price):\n        # TODO: delegate to self.discount\n        pass\n",
                    "example": "Cart(PercentOff(10)).checkout(100) -> 90.0",
                    "tests": [
                        {"name": "no discount", "code": "assert Cart(NoDiscount()).checkout(100) == 100"},
                        {"name": "percent off", "code": "assert Cart(PercentOff(10)).checkout(100) == 90.0"},
                        {"name": "strategy is swappable", "code": "assert Cart(PercentOff(50)).checkout(200) == 100.0"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "How would you design a notification system that supports email, SMS, and push, and can add new channels later without modifying existing code?",
                        "hint": "Combine Factory (to create the right notifier) with a shared interface (Strategy/abstraction) each notifier implements.",
                        "model_answer": "Define a common `Notifier` interface (ABC) with a `send(message)` method. Each channel (`EmailNotifier`, `SMSNotifier`, `PushNotifier`) implements it - that's Strategy: swappable behavior behind one interface. Use a Factory function/registry to map a channel name to its class, so adding a new channel means adding one new class and one registry entry, not touching a big if/elif chain - satisfying the Open/Closed Principle too.",
                    },
                    {
                        "id": "i2",
                        "question": "What's the difference between the Strategy pattern and simply passing a function as a parameter (higher-order functions)?",
                        "hint": "Think about when a strategy needs its own state or multiple related methods, versus when a single function is enough.",
                        "model_answer": "They solve the same core problem (swappable behavior) and in Python are often interchangeable for simple cases - you can pass a plain function instead of a Strategy object. The class-based Strategy pattern earns its keep when the algorithm needs its own state/configuration or several related methods that should travel together (e.g. `PercentOff` carrying its `percent`), where a single function parameter would need extra closures or partials to do the same job.",
                    },
                ],
            },
            {
                "id": "metaclasses-and-mro",
                "title": "Metaclasses & MRO",
                "tagline": "The machinery that builds classes themselves",
                "theory": """
Everything in Python is an object - including classes themselves. The class of a class is called its
**metaclass**, and by default that's `type`:

```python
class Dog:
    pass

type(Dog)        # <class 'type'>
type(Dog())      # <class '__main__.Dog'>
```

`type` can also be called directly to create a class dynamically: `type("Dog", (), {})` is equivalent to
`class Dog: pass`. A custom metaclass subclasses `type` and can override `__new__`/`__init__` to control
*how classes themselves get built* - e.g. auto-registering every subclass, validating that required
methods exist, or auto-adding methods:

```python
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        cls.registry.append(cls) if hasattr(cls, "registry") else None
        return cls
```

In practice, most "I need a metaclass" problems are actually solved more simply with `__init_subclass__`
(a hook that runs automatically whenever a class is subclassed, no metaclass required) or class decorators.
The senior-engineer answer is usually "here's what a metaclass *could* do, but here's the simpler tool I'd
actually reach for" - ABCs themselves are implemented via a metaclass (`ABCMeta`) under the hood.

**MRO** (Method Resolution Order) is the deterministic order Python searches through a class's ancestors
to resolve an attribute/method lookup, computed with the **C3 linearization** algorithm. It guarantees:
a class always appears before its parents, and if a class inherits from multiple parents, their relative
order is preserved. You can always inspect it directly: `SomeClass.__mro__` or `SomeClass.mro()`.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "What is a metaclass?",
                        "options": [
                            {"id": "a", "text": "A class with only static methods"},
                            {"id": "b", "text": "The class of a class - the thing responsible for constructing class objects themselves, by default `type`"},
                            {"id": "c", "text": "A synonym for an abstract base class"},
                            {"id": "d", "text": "A class that cannot be instantiated"},
                        ],
                        "correct": "b",
                        "explanation": "Just like an object is an instance of a class, a class is an instance of its metaclass - by default `type`, but you can subclass `type` to customize class creation itself.",
                    },
                    {
                        "id": "q2",
                        "question": "What's usually the simpler, more idiomatic alternative to writing a custom metaclass just to run code whenever a class is subclassed?",
                        "options": [
                            {"id": "a", "text": "__init_subclass__"},
                            {"id": "b", "text": "__new__"},
                            {"id": "c", "text": "@staticmethod"},
                            {"id": "d", "text": "There is no simpler alternative"},
                        ],
                        "correct": "a",
                        "explanation": "`__init_subclass__` is a classmethod hook, added in Python 3.6+, that runs automatically for every subclass - it covers the majority of cases people reach for metaclasses for, with far less complexity.",
                    },
                    {
                        "id": "q3",
                        "question": "What algorithm does Python use to compute a class's MRO when multiple inheritance is involved?",
                        "options": [
                            {"id": "a", "text": "Simple depth-first left-to-right search"},
                            {"id": "b", "text": "C3 linearization"},
                            {"id": "c", "text": "Breadth-first search"},
                            {"id": "d", "text": "Alphabetical ordering of base class names"},
                        ],
                        "correct": "b",
                        "explanation": "C3 linearization guarantees a consistent, monotonic order where a class precedes its parents and relative parent order is preserved - you can inspect the result with `ClassName.__mro__`.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Using `__init_subclass__`, write a base `Plugin` class that automatically appends every subclass to a class-level list `Plugin.registry` as soon as it's defined (no need to instantiate the subclass).",
                    "starter_code": "class Plugin:\n    registry = []\n\n    def __init_subclass__(cls, **kwargs):\n        super().__init_subclass__(**kwargs)\n        # TODO: append cls to Plugin.registry\n        pass\n",
                    "example": "class A(Plugin): pass\nclass B(Plugin): pass\nPlugin.registry -> [A, B]",
                    "tests": [
                        {"name": "subclasses auto-register", "code": "Plugin.registry.clear()\nclass A(Plugin):\n    pass\nclass B(Plugin):\n    pass\nassert Plugin.registry == [A, B]"},
                        {"name": "base class itself is not registered", "code": "Plugin.registry.clear()\nassert Plugin.registry == []"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "Have you ever needed a metaclass in real code, or would __init_subclass__ / a class decorator have done the job? How do you decide?",
                        "hint": "Metaclasses are rarely truly necessary - be honest about when the simpler tool wins.",
                        "model_answer": "Metaclasses are genuinely needed when you must control the class creation process itself in ways `__init_subclass__` can't reach - e.g. changing the namespace dict before the class body executes, or when building a framework like an ORM that needs deep control over attribute processing at class-definition time (Django's ORM does this). For the common case of 'run code when a subclass is defined' or 'validate/register subclasses', `__init_subclass__` is simpler, more discoverable, and the better default.",
                    },
                    {
                        "id": "i2",
                        "question": "Explain the diamond inheritance problem and how Python's MRO resolves it.",
                        "hint": "Picture class D(B, C) where both B and C inherit from A.",
                        "model_answer": "If `B` and `C` both inherit from `A`, and `D` inherits from both `B` and `C`, a naive lookup could reach `A` through two different paths, risking `A`'s method running twice or an ambiguous order. Python's C3-linearized MRO resolves this deterministically and consistently: for `class D(B, C)`, the MRO is `D, B, C, A, object` - each class appears exactly once, before its own parents, and in an order consistent with how the class was declared. `super()` walks this single linear order rather than the raw inheritance graph, which is what prevents `A` from being visited twice.",
                    },
                ],
            },
            {
                "id": "oop-system-design",
                "title": "OOP System Design",
                "tagline": "Full interview-style design problems",
                "theory": """
The "design a parking lot" / "design a library system" style question is where every earlier topic gets
combined and tested at once. Interviewers are evaluating your *process*, not just the final class diagram.
A solid approach:

1. **Clarify scope and requirements first.** What are the core entities? What operations must be
   supported? What's explicitly out of scope? (e.g. "Does the parking lot need to handle payments, or just
   track occupancy?")

2. **Identify the nouns as candidate classes**, and the verbs as candidate methods. For a parking lot:
   `ParkingLot`, `Level`, `Spot`, `Vehicle` (with subclasses `Car`, `Motorcycle`), `Ticket`.

3. **Decide relationships deliberately**: is it inheritance (`Car is-a Vehicle`) or composition
   (`ParkingLot has Levels`, `Level has Spots`)? Justify each choice out loud.

4. **Apply the principles as they become relevant**, not as a forced checklist:
   - Abstraction: an abstract `Vehicle` or `PaymentStrategy` if behavior varies by type.
   - Single Responsibility: separate `Ticket` (data) from `PricingStrategy` (calculation) from
     `ParkingLot` (orchestration).
   - Open/Closed: adding a new vehicle type or a new pricing scheme shouldn't require editing existing
     classes.

5. **Talk through edge cases**: lot is full, vehicle doesn't fit any spot size, concurrent access from two
   entry gates.

The biggest interview differentiator isn't knowing more vocabulary - it's *narrating your reasoning* as you
go: "I'm modeling this as composition because a Level doesn't behave like a Spot, it just contains them,"
rather than silently drawing a diagram.
""".strip(),
                "quiz": [
                    {
                        "id": "q1",
                        "question": "In an OOP system design interview, what should you typically do first?",
                        "options": [
                            {"id": "a", "text": "Immediately start writing class definitions in code"},
                            {"id": "b", "text": "Clarify requirements and scope before identifying entities"},
                            {"id": "c", "text": "Pick which design patterns to use before understanding the problem"},
                            {"id": "d", "text": "Ask what programming language the interviewer prefers"},
                        ],
                        "correct": "b",
                        "explanation": "Jumping straight to classes without agreeing on scope is the most common mistake - requirements determine which entities and relationships actually matter.",
                    },
                    {
                        "id": "q2",
                        "question": "In a 'design a parking lot' problem, how would you typically model the relationship between ParkingLot and Level, and between Level and Spot?",
                        "options": [
                            {"id": "a", "text": "Inheritance: Level extends ParkingLot, Spot extends Level"},
                            {"id": "b", "text": "Composition: ParkingLot has Levels, Level has Spots"},
                            {"id": "c", "text": "No relationship needed, they're all independent"},
                            {"id": "d", "text": "Multiple inheritance from a shared Structure base class"},
                        ],
                        "correct": "b",
                        "explanation": "None of these is truly a kind of the other (a Level isn't a kind of ParkingLot) - they're containment/has-a relationships, which is composition's job.",
                    },
                    {
                        "id": "q3",
                        "question": "In the same problem, you want to support adding a new pricing scheme later (e.g. hourly vs flat-rate) without modifying ParkingLot's code. Which principle and pattern combination fits best?",
                        "options": [
                            {"id": "a", "text": "Liskov Substitution alone, no pattern needed"},
                            {"id": "b", "text": "Open/Closed Principle, implemented via the Strategy pattern (a PricingStrategy interface with swappable implementations)"},
                            {"id": "c", "text": "Singleton pattern applied to ParkingLot"},
                            {"id": "d", "text": "Deep inheritance from a base PricingLot class"},
                        ],
                        "correct": "b",
                        "explanation": "This is the same shape as the earlier Strategy topic, applied in a system-design context: pluggable pricing behind one interface means new pricing schemes are pure extension, not modification.",
                    },
                ],
                "challenge": {
                    "id": "c1",
                    "prompt": "Model a tiny slice of a parking lot: an abstract `Vehicle` with attribute `size` ('small' or 'large'), a `Spot` class with `size` and `occupied=False`, and a method `park(self, vehicle)` on `Spot` that sets `occupied = True` and returns `True` if `vehicle.size == self.size` and the spot isn't already occupied, otherwise returns `False` without changing state.",
                    "starter_code": "class Vehicle:\n    def __init__(self, size):\n        self.size = size\n\nclass Spot:\n    def __init__(self, size):\n        self.size = size\n        self.occupied = False\n\n    def park(self, vehicle):\n        # TODO: return True and occupy the spot only if size matches and it's free\n        pass\n",
                    "example": "Spot('small').park(Vehicle('small')) -> True",
                    "tests": [
                        {"name": "matching size parks successfully", "code": "s = Spot('small')\nassert s.park(Vehicle('small')) == True\nassert s.occupied == True"},
                        {"name": "mismatched size fails without occupying", "code": "s = Spot('small')\nassert s.park(Vehicle('large')) == False\nassert s.occupied == False"},
                        {"name": "already occupied spot rejects new vehicle", "code": "s = Spot('small')\ns.park(Vehicle('small'))\nassert s.park(Vehicle('small')) == False"},
                    ],
                },
                "interview": [
                    {
                        "id": "i1",
                        "question": "Design a library system: what are the core classes, and how do Book, BookCopy, and Member relate to each other?",
                        "hint": "Distinguish the abstract 'Book' (title/author/ISBN) from a physical 'BookCopy' (one shelvable, loanable item) - a very common real detail interviewers listen for.",
                        "model_answer": "Core entities: `Book` (title, author, ISBN - the abstract work), `BookCopy` (one physical copy of a Book, with its own status: available/checked-out), `Member` (has a list of current loans), and `Loan` (links a Member to a BookCopy with due/return dates). The key detail interviewers listen for: a library owns multiple physical *copies* of the same *book*, so `Book` and `BookCopy` must be separate classes (composition: a Book has many BookCopies), not conflated into one - conflating them is the most common mistake in this exact problem.",
                    },
                    {
                        "id": "i2",
                        "question": "In any system design interview, how do you decide when a relationship should be inheritance vs composition vs just a reference/ID?",
                        "hint": "Combine the 'is-a' test from the Composition topic with a practical lens on lifecycle and ownership.",
                        "model_answer": "Ask three questions in order: (1) Is it truly 'is-a', substitutable everywhere the parent is used? If yes, inheritance. (2) Does the containing object *own* the lifecycle of the other (created/destroyed together, e.g. ParkingLot and its Levels)? If yes, composition. (3) Does it just need to *point to* another independently-existing object (e.g. a Loan referencing a Member who exists regardless of any particular loan)? Then a simple reference/foreign key is enough - don't force composition or inheritance where a plain association will do.",
                    },
                ],
            },
        ],
    },
]


def get_all_topics():
    """Flatten (level, topic) pairs for lookup by topic id."""
    out = {}
    for level in LEVELS:
        for topic in level["topics"]:
            out[topic["id"]] = {"level": level, "topic": topic}
    return out


TOPICS_BY_ID = get_all_topics()
