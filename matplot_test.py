import js
from js import document

# Importing numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Create an array
arr = np.array([1, 2, 3, 4, 5])

# Perform some operations
mean = np.mean(arr)
sum_values = np.sum(arr)

# Generate a simple Matplotlib plot
plt.plot(arr)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Sample Plot')

# Convert the Matplotlib plot to an image format
fig = plt.gcf()
fig.canvas.draw()
img_data = fig.canvas.tostring_rgb()
img_width, img_height = fig.canvas.get_width_height()

# Encode the image data as base64 using JavaScript's btoa() function
js_code = f"btoa('{img_data.decode('latin-1')}')"
img_base64 = js.eval(js_code)

# Create an HTML <img> element and set its src attribute to display the image
img_element = document.createElement("img")
img_element.src = f"data:image/png;base64,{img_base64}"

# Append the <img> element to the "test" <div>
x = document.getElementById("test")
x.appendChild(img_element)

# Display the results in the HTML
x.textContent = "Array: " + str(arr)
x.textContent += "\nMean: " + str(mean)
x.textContent += "\nSum: " + str(sum_values)
