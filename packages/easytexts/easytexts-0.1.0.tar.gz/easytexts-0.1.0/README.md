				---------------------------------------------------

									  Easytexts

				---------------------------------------------------

Easytexts is a Python module created for learning and completing small-scale projects that involve text files.
It provides convenient functions for managing text files without the complexity Python's built in system.
Use it to explore text file handling and get your project tasks done efficiently!


				---------------------------------------------------

									  Usage

				---------------------------------------------------

Import the Easytexts module in your Python script:


from easytexts import *

Here are the available functions:

1. Writing and Appending:

append(location_and_name, text): Adds text to the end of a file.

rewrite(location_and_name, text): Overwrites the entire content of a file with new text.

create_if_doesnt_exist(location_and_name, text): Creates a new file and writes text to it, handling existing files gracefully.

2. Reading:

read(location_and_name): Reads the entire content of a file and returns it as a string.

3. Clearing and Checking:

clear(location_and_name): Empties the content of a file.

is_clear(location_and_name): Checks if a file is empty (returns True if empty, False otherwise).

4. Deleting:

delete(location_and_name): Deletes a file.

5. Checking Existence:

does_exist(location_and_name): Checks if a file exists (returns True if exists, False otherwise).


Examples
Here are some examples of how to use Easytext:


# Append text to a file
append("my_file.txt", "This is a new line added to the file.\n")

# Rewrite the content of a file
rewrite("my_file.txt", "This is the new content.\n")

# Create a new file with text
create_if_doesnt_exist("new_file.txt", "Hello, world!\n")

# Read the contents of a file
content = read("my_file.txt")
print(content)

# Clear a file
clear("my_file.txt")

# Check if a file is empty
if is_clear("my_file.txt"):
    print("The file is empty.")

# Delete a file
delete("old_file.txt")

# Check if a file exists
if does_exist("my_file.txt"):
    print("The file exists.")
	


