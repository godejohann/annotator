# Annotator
The Annotator is a simple GUI-based application that allows you to annotate images for image classification. The application allows the user to select a directory containing images and then display the images one by one, allowing the user to label each image with one of two predefined classes. Additionally, it allows the user to select one or multiple flags from a predefined hierarchy, representing objects present in the image. The code and this documentation are written with the help of ChatGPT.

# Requirements
- Python 3.8+
- Tkinter 8.5+
- PIL 9.4+

# Usage
1. Run the annotator.py script.
2. Select a directory containing images by clicking the "Select" button.
3. Navigate through the images using the "Back" and "Next" buttons.
4. Label the current image by selecting one of the two classes.
5. Flag the current image by selecting one or multiple flags from the TreeView.
6. Save the annotations to a json file by clicking the "Save" button.

# Annotation Format
The annotations are saved in a json file with the following format:

```json
{
    "filename1": {"labels": {"label": "Negative"}, "flags": ["Foo/Bar/foo_bar_1"]},
    "filename2": {"labels": {"label": "Positive"}, "flags": ["Foo/Bar/foo_bar_2"]},
    ...
}
```

- Each key in the json object represents the filename of an image.
- The value of each key is another json object, representing the annotation of the corresponding image.
- The annotation json object has two keys, 'labels' and 'flags'.
- The key 'labels' contains a dictionary with key 'label' and a string value of 'Positive' or 'Negative' representing whether the given image corresponds to a positive or negative example.
- The key 'flags' contains a list of strings, representing objects present in the corresponding image.

# Flags Hierarchy
The script flags_hierarchy.py contains a single variable, 'hierarchy'. The 'hierarchy' variable is a nested dictionary, representing a tree structure of the flags. It is used to dynamically create the TreeView, representing the flags hierarchy. The flags can be customized to the corresponding image classification task.

# Limitations
- The application can only handle two classes at the moment.
