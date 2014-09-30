SpyMyWeb
========
Now you can see what's going on your local internet, if you're curious about what people are seeing in their computer you can use Wireshark to capture their packets and then, use "packetExtractor.py" to extract only the images then upload to SpyMyWeb Local Website.

Pay attention to "config.cfg" file, you need to setup the website IP and Port, and your proxy network.

*Obs.: For a clean run it's adviced to copy "default.html" content inside "index.html"

-> Explanations
-"packetExtractor.py": Read "pacotes.txt" file (packets) and extract only packet related to images, and using Full Request URI field the image is downloaded by urllib module. After each download, the image is opened and sent attached with a POST header.

-"LOG webserver.py": Wait for GET or POST requisitions. In POST, the received image is written with your original name of url. Homepage is update after each new image received, and a logfile is created showing how works receiving packets process.

