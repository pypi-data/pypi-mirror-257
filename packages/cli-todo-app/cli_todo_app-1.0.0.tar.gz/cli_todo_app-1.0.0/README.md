# CLI Todo App

A simple, cli todo tool written in python3. Written to be simple yet has quite handy features. 


## Specification

1. This app can be run in the console with `python3 -m todo [arguments]`(for *nix) and `python -m todo [argumnents]`(for Windows).

2. This app reads from and write to a `todo.txt` text file. Each todo item occupies a single line in this file. Here is an example file that has 2 todo items.

```txt
[2]water the plants
[1]change light bulb
```

3.  When a todo item is marked completed, it is removed from `todo.txt` and instead added to the `done.txt` text file. This file has a different format:

    ```txt
    x 2020-06-12 the text contents of the todo item
    ```

    1. the letter x
    2. the current date (UTC/GMT) in `yyyy-mm-dd` format
    3. the original text

    The date when the todo is marked as completed is recorded in the `yyyy-mm-dd` format (ISO 8601). For example, a date like `15th August, 2020` is represented as `2020-08-15`.

4.  This application opens the files `todo.txt` and `done.txt` from where the app is run, and not where the app is located. For example, if we invoke the app like this:

    ```
    $ cd /path/to/plans
    $ /path/to/apps/todo ls
    ```

    This application looks for the text files in `/path/to/plans`, since that is the user’s current directory.

## Usage

### 1. Help command - prints the CLI usage.

```
$ ./todo help
Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics
```
Note:-Executing the file without any arguments, or with a single argument `help` triggers this command


### 2. ls command - list all pending todos

Use the `ls` command to see all the todos that are not yet complete. The most recently added todo are displayed first.

```
$ ./todo ls
[2] change light bulb
[1] water the plants
```

### 3. Add a new todo - adds a new todo item

Use the `add` command. The text of the todo item should be enclosed within double quotes (otherwise only the first word is considered as the todo text, and the remaining words are treated as different arguments).

```
$ ./todo add "the thing i need to do"
Added todo: "the thing i need to do"
```

### 4. Delete a todo item

Use the `del` command to remove a todo item by its number.

```
$ ./todo del 3
Deleted todo #3
```

Attempting to delete a non-existent todo item should display an error message.

```
$ ./todo del 5
Error: todo #5 does not exist. Nothing deleted.
```

### 5. Mark a todo item as completed

Use the `done` command to mark a todo item as completed by its number.

```
$ ./todo done 1
Marked todo #1 as done.
```

Attempting to mark a non-existed todo item as completed will display an error message.

```
$ ./todo done 5
Error: todo #5 does not exist.
```

### 6. Generate a report

Use the `report` command to see the latest tally of pending and completed todos.

```
$ ./todo report
yyyy-mm-dd Pending : 1 Completed : 4
```

## License
This project is licensed under [Apache License2.0](https://apache.org/licenses/LICENSE-2.0).


## Contributing
Project contribution can be made  by forking the repository and making a pull request. The merge code will be thoroughly tested and then merged to respective branch(except master).

## Project Status
The project is being actively developed by the author(s) depending upon their availability. We as community can make opensource software accessible and reliable for all.
