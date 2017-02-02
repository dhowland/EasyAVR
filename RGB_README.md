## RGB LED support

To add RGB LED support, add the following to a board file:


`use_rgb = True`

`rgb_pin = pin_to_binary(pin)`, where `pin` is the output (e.g. C7) (untested for ports other than C!)

`rgb_count = count`, where `count` is the number of RGB LEDs on the board

`rgb_max = max`, where `max` is the maximum allowed brightness for any LED (R+G+B) (set to 255*3 for uncapped)

`rgb_url = url`, where `url` is a string containing the URL for a keyboard-layout-editor configurator. [See this example.](http://www.keyboard-layout-editor.com/#/gists/437edbad91365c9ef7b2)

`rgb_order = order`, where order is a list of integers. Set this up so that order[x] = y, where x is the physical location of the LED in the chain and y is the visual location in KLE (counting left to right, top to bottom).
