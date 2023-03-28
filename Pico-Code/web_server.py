import ring_light, network, socket

DEFAULT_HTML = "<!DOCTYPE html><html>Set HTML value in web_server class...</html>"


class web_server:
    def __init__(self, ssid, password):
        self.SSID = ssid
        self.WIFI_PASSWORD = password

        self.__connect()
        self.__open_socket()
        self.root_folder = "web"
        self.html = DEFAULT_HTML
        ring_light.waiting_for_impact()

    def serve(self):
        client = self.connection.accept()[0]
        request = client.recv(1024)
        request = str(request)

        css_count = self.__clamp_count(request.find(".css"))
        font_count = self.__clamp_count(request.find(".ttf"))
        image_count = self.__clamp_count(request.find(".png") + request.find(".jpg"))

        print(request + "\n")

        print("css_count: " + str(css_count) + "\n")
        print("font_count: " + str(font_count) + "\n")
        print("image_count: " + str(image_count) + "\n")
        print("Fulfilled: ")

        # Check for CSS requests
        if css_count != 1000 and min(css_count, font_count, image_count) == css_count:
            css_file = self.root_folder + request[6 : css_count + 4]
            css_file = open(css_file, "r")
            client.send(css_file.read())
            print("CSS\n")
            client.close()
            return

        # Check for Image requests
        if css_count != 1000 and min(css_count, image_count, font_count) == image_count:
            image_file = self.root_folder + request[6 : image_count + 4]
            client.send(image_file)
            client.close()
            print("IMG\n")
            return

        # Check for Font requests
        if css_count != 1000 and min(css_count, image_count, font_count) == font_count:
            print("FONT\n")
            client.close()
            return

        client.send(self.html)
        print("HTML\n")
        client.close()

    def __connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.SSID, self.WIFI_PASSWORD)

        while wlan.isconnected() == False:
            print("Waiting for connection...")
            ring_light.waiting_for_connection()

        self.LOCAL_IP = wlan.ifconfig()[0]
        print(f"Connected on {self.LOCAL_IP}")

    def __open_socket(self):
        address = (self.LOCAL_IP, 80)
        self.connection = socket.socket()
        self.connection.bind(address)
        self.connection.listen(1)

    def __clamp_count(self, count):
        if count < 0:
            return 1000
        return count

    def set_html(self, html):
        self.html = html
