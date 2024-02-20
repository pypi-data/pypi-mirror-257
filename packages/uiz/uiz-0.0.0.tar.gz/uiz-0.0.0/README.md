# UIZ

### A simple UI module built off PyQt5

uiz is a simple GUI/UI module built using PyQt5. uiz is designed to be simple, and opensource. You can check out the code on GitHub at zPointless/

```
# Instantiate the App
app = App()

# Create a window
window = app.newWindow("Demo Window", 800, 600)

# Button press function
def onPress():
    webv.setHTML(textarea.getText())

# Examples of each element

# Button
button = Elements.Button('Show HTML', onPress, font="Arial")
button.move(50, 50)
window.showElement(button)

# Text Area
textarea = Elements.TextArea('HTML from Text', font="Arial")
textarea.setGeometry(50, 100, 300, 200)
window.showElement(textarea)

# WebView
webv = Elements.WebView()
webv.setGeometry(400, 100, 300, 200)
webv.setHTML('<h1>Welcome to the WebView!</h1>')
window.showElement(webv)

# Image
img = Elements.Image('path/to/your/image.jpg')  # Adjust the path accordingly
img.setGeometry(50, 350, 300, 200)
window.showElement(img)

# Checkbox
checkbox = Elements.Checkbox('Check me')
checkbox.setGeometry(400, 350, 100, 30)
window.showElement(checkbox)

# RadioButton
radio_button = Elements.RadioButton('Radio Button')
radio_button.setGeometry(550, 350, 150, 30)
window.showElement(radio_button)

# ComboBox
combo_box = Elements.ComboBox(['Option 1', 'Option 2', 'Option 3'])
combo_box.setGeometry(50, 550, 150, 30)
window.showElement(combo_box)

# ProgressBar
progress_bar = Elements.Progressbar()
progress_bar.setGeometry(250, 550, 200, 30)
progress_bar.setValue(50)
window.showElement(progress_bar)

# Slider
slider = Elements.Slider()
slider.setGeometry(500, 550, 200, 30)
slider.setValue(75)
window.showElement(slider)

# Run the application
app.run()
```