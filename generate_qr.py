import qrcode

ip_address = "http://192.168.33.97:5000"
qr = qrcode.make(ip_address)
qr.save("ip_qr.png")