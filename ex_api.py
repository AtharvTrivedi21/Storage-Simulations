from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# In-memory storage (for demonstration)
stored_values = []
global_depth = 1
bucket_size = 2
directory = {'0': [], '1': []}


# Hashing function
def hash_value(value, depth):
    return bin(value % (2 ** depth))[2:].zfill(depth)


# Rehash function with local depth based on the number of elements in the bucket
def rehash():
    global global_depth, directory, stored_values

    # Clear all existing buckets
    for bucket in directory:
        directory[bucket].clear()

    # Insert all values into the current directory
    for value in stored_values:
        index = hash_value(value, global_depth)

        # If the bucket has space, add the value
        if len(directory[index]) < bucket_size:
            directory[index].append(value)
        else:
            # Perform a bucket split
            global_depth += 1  # Increase global depth

            # Re-create the directory with more bits
            new_directory = {}
            for i in range(2 ** global_depth):
                new_directory[bin(i)[2:].zfill(global_depth)] = []

            # Re-insert all values
            for val in stored_values:
                new_index = hash_value(val, global_depth)
                new_directory[new_index].append(val)

            directory = new_directory
            break


class ValueItem(BaseModel):
    value: int


@app.get("/directory")
def get_directory():
    # Format the directory output into the desired structure
    result = []
    for bucket_index, values in directory.items():
        # Show the bucket and its values
        result.append(f"Bucket {bucket_index}")
        result.append(f"Values: {', '.join(map(str, values)) if values else ''}")
        
        # Local Depth should show the number of elements in each bucket
        local_depth = len(values)  # Count of elements in the bucket
        result.append(f"Local Depth: {local_depth}")

    # Join the result into a single formatted string with line breaks
    formatted_output = "\n".join(result)
    
    # Return both the directory structure and the formatted output
    return {"global_depth": global_depth, "directory": directory, "formatted_directory": formatted_output}


@app.post("/insert")
def insert_value(item: ValueItem):
    global stored_values
    stored_values.append(item.value)
    rehash()
    # Return the directory without the 'directory_display' or any other renamed key
    return {"message": f"Value {item.value} inserted", "directory": get_directory()["directory"]}


@app.post("/delete")
def delete_value(item: ValueItem):
    global stored_values
    if item.value in stored_values:
        stored_values.remove(item.value)
        rehash()
        return {"message": f"Value {item.value} deleted", "directory": get_directory()["directory"]}
    return {"message": f"Value {item.value} not found", "directory": get_directory()["directory"]}

@app.post("/clear")
def clear_storage():
    global stored_values, global_depth, directory

    # Clear all stored values
    stored_values.clear()

    # Reset global depth and directory
    global_depth = 1  # Reset to initial depth
    directory = {'0': [], '1': []}  # Reset directory to two empty buckets

    return {"message": "All values cleared successfully. Buckets reset to default."}
