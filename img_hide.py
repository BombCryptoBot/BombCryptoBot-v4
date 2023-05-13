import cv2
import base64

def char_generator(message):
  for c in message:
    yield ord(c)

def get_image(image_location):
  img = cv2.imread(image_location)
  return img

def gcd(x, y):
  while(y):
    x, y = y, x % y
  return x

def encode_image(image_location, msg):
  img = get_image(image_location)
  msg_gen = char_generator(msg)
  pattern = gcd(len(img), len(img[0]))
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i+1 * j+1) % pattern == 0:
        try:
          img[i-1][j-1][0] = next(msg_gen)
        except StopIteration:
          img[i-1][j-1][0] = 0
          return img

def decode_image(img_loc):
  img = get_image(img_loc)
  pattern = gcd(len(img), len(img[0]))
  message = ''
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i-1 * j-1) % pattern == 0:
        if img[i-1][j-1][0] != 0:
          message = message + chr(img[i-1][j-1][0])
        else:
          return message

def get_crypt_key(key):
	tmp1 = key[:(int(len(key)/2))][::-1]
	tmp2 = key[(int(len(key)/2)):][::-1]
	return tmp2 + tmp1

with open('./keys/bot.pub', 'r') as file:
    x = get_crypt_key(file.read().rstrip())
    key = base64.b64encode(x.encode()).decode("utf-8")
    privKey = get_crypt_key(key)
    x = encode_image("./dist/images/loading_logo.png", privKey)
    cv2.imwrite("./dist/images/loading_logo.png", x);
    print("Key stored in image")
