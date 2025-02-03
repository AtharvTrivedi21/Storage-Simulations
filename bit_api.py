from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class BitmapIndex:
    def __init__(self, num_attributes):
        self.num_attributes = num_attributes
        self.index = {i: [] for i in range(num_attributes)}
        self.data = []
        self.unique_values = set()  # Track unique values inserted

    def insert(self, value):
        self.data.append(value)
        self.unique_values.add(value)  # Add value to unique values

        # Extend bitmaps with 0s if the index for that value doesn't exist
        for attr in self.index.keys():
            if len(self.index[attr]) < len(self.data):
                self.index[attr].append(0)  # Fill with zeros for the new entry

            # Set bitmap for the inserted value's corresponding attribute
            if attr == value:
                self.index[attr][-1] = 1  # Set 1 for the inserted value's corresponding attribute

    def delete(self, value):
        if value in self.data:
            indices_to_delete = [i for i, v in enumerate(self.data) if v == value]
            for index in sorted(indices_to_delete, reverse=True):
                self.data.pop(index)  # Remove the value from the data list
                for bitmap in self.index.values():
                    bitmap.pop(index)  # Remove the corresponding bit
            self.unique_values.discard(value)  # Remove value from unique values
        else:
            raise ValueError("Value not found")

    def search(self, value):
        if value in self.unique_values:
            indices = [i for i, v in enumerate(self.data) if v == value]
            return indices
        else:
            raise ValueError("Value not found")

    def display(self):
        """Display the bitmap index for unique values only."""
        formatted_result = []
        for value in sorted(self.unique_values):
            if value in self.index:
                formatted_result.append(f"Attribute {value}: {self.index[value]}")
        return formatted_result

app = FastAPI()

bitmap_index = BitmapIndex(num_attributes=100)  # Adjusted to allow for a wider range

class ValueModel(BaseModel):
    value: int

@app.post("/insert")
def insert_value(value_model: ValueModel):
    if value_model.value < 0:
        raise HTTPException(status_code=400, detail="Only non-negative integers are allowed.")
    bitmap_index.insert(value_model.value)
    return {"message": f"Inserted value {value_model.value}"}

@app.post("/delete")
def delete_value(value_model: ValueModel):
    try:
        bitmap_index.delete(value_model.value)
        return {"message": f"Deleted value {value_model.value}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/search")
def search_value(value_model: ValueModel):
    try:
        indices = bitmap_index.search(value_model.value)
        return {"indices": indices}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/display")
def display_index():
    """Display the bitmap index with formatted output for unique values only."""
    result = bitmap_index.display()
    if not result:
        return {"message": "The bitmap index is currently empty."}
    return result
