from functions import *

class BombCryptoBot():
	# User variables
	metamask_pass = False
	lang_sel = "en"
	pathfind_renew_interval = 3
	hero_test_after_maps = 5
	hero_test_after_mins = 20

	chest_delay = 60
	min_stam = 25
	debugVar = False
	wait_loading = 60

	# Time variables
	key_validated = False
	last_ping_pong = 0
	last_pathfind = None
	start_work = None

	# Bot Variables
	metamask_extension_id = "nkbihfbeogaeaoehlefnkodbefgpgknn"
	pro = False
	loading_detected = False
	wallet_unlocked = False
	wallet_connected = False
	able_to_work = False
	showDisplay = True
	ping_errors = 0

	# House variables
	use_house=0
	maps_passed=0
	account_heroes=0

	# Schoolar
	username = False
	password = False

	video_feed = False

	last_chest_check = 0
	last_hero_check = 0
	pro = False

	def __init__(self, args):
		print_banner()

		if 'lang' in args:
			self.lang_sel = args['lang']
		self.lang = self.load_lang()

		if 'key' not in args:
			self.debug(self.lang.messages['error_validation_bombcrypto_bot'], self.lang.messages['error'])

		self.key = args['key']
		self.instance_name = args['instance_name'] if 'instance_name' in args and args['instance_name'] != None else ""
		if self.instance_name == "":
			self.debug(self.lang.messages['error_no_instance_name'])
			exit()

		if f'username' in args and f'password' in args:
			self.username = args[f'username'] if len(args[f'username']) > 0 else False
			self.password = args[f'password'] if len(args[f'password']) > 0 else False
		if 'metamask_pass' in args:
			self.metamask_pass = args['metamask_pass'] if 'metamask_pass' in args and args['metamask_pass'] != None else False
		if 'pathfind_renew_interval' in args:
			self.pathfind_renew_interval = int(args['pathfind_renew_interval'])
		if 'hero_test_after_mins' in args:
			self.hero_test_after_mins = int(args['hero_test_after_mins'])
		if 'hero_test_after_maps' in args:
			self.hero_test_after_maps = int(args['hero_test_after_maps'])
		if 'min_stam' in args:
			self.min_stam = int(args['min_stam'])
		if 'debug' in args:
			self.debugVar = args['debug']
		if 'showDisplay' in args:
			self.showDisplay = True if int(args['showDisplay']) == 1 else False
		if 'wait_loading' in args:
			self.wait_loading = int(args['wait_loading'])
		if 'account_heroes' in args:
			self.account_heroes = int(args['account_heroes'])
		if 'use_house' in args:
			self.use_house = True if int(args['use_house']) == 1 else False
			
		self.hero_test_random = random.randint(math.floor(self.hero_test_after_mins*0.75), self.hero_test_after_mins)
		self.chest_delay_rand = random.randint(math.floor(self.chest_delay*0.75), self.chest_delay)

		# RSA Load
		try:
			self.bot_rsa_public = RSA.importKey(self.decode_string(decode_image(self.decode_string("==gLvkWbhdWZz9CbvFGZp52Zfx2bn9mLw52Z"))))
			self.api_url = self.decode_string("oRHdwNnOv8CdoVmYvR3cvNWalRXeu4WZ09SYwl2L")
			self.key_crypt = self.get_crypt_key(self.key)
		except:
			self.quit()
		self.start()

	def debug(self, message=None, type="LOG"):
		msg = f"{datetime.now()} [{self.instance_name}/{type}] {message}"
		print(msg)
		file_object = open('./bot.log', 'a')
		file_object.write(f"{msg}\n")
		file_object.close()
		return True

	def start(self):
		if not self.key_validated:
			self.debug(self.lang.messages['validating_bombcrypto_bot_account'])
			self.key_validated = self.validate()
			if self.key_validated:
				self.last_ping_pong = time.time()
			else:
				self.debug(self.lang.messages['error_validation_bombcrypto_bot'], self.lang.messages['error'])

		if self.key_validated:
			if os.name != "nt" and self.showDisplay:
				self.display = display_start(True)
			else:
				self.display = False

			if not self.startBrowser():
				return self.restart()
			if not self.start_game():
				return self.restart()
			self.able_to_work = True
			if not self.play():
				return self.restart()

		print("Stopping bot")
		self.quit()

	def restart(self):
		sleep(1)
		# Restart bot variables
		self.loading_detected = False
		self.wallet_unlocked = False
		self.wallet_connected = False
		self.able_to_work = False
		self.last_chest_check = 0
		self.last_hero_check = 0
		self.last_pathfind = time.time()
		self.last_chest_check = time.time()
		try:
			self.chrome.quit()
		except:
			pass
		return self.start()

	def quit(self):
		try:
			self.chrome.quit()
		except:
			pass
		try:
			display_stop(self.display)
		except:
			pass
		exit()

	def startBrowser(self):
		tmp_path = os.getcwdb().decode("utf-8") + f"/profiles/{self.instance_name}"
		if not os.path.isdir(tmp_path):
			os.makedirs(tmp_path)
		else:
			if os.path.isdir(f"{tmp_path}/Default/Cache"):
				rmdir(f"{tmp_path}/Default/Cache")

		chromedriver = "./chromedriver.exe" if os.name == 'nt' else "./chromedriver"
		if not file_exists(chromedriver):
			self.debug(self.lang.messages['error_no_chromedriver'])
			sleep(3)
			return False

		self.chrome = get_chrome_drive(profile_path=tmp_path, driver_path=chromedriver, headless=False)

		if (self.username and self.password):
			return True

		if self.unlock_wallet():
			return True
		return False

	def validate(self, ping=False):
		if ping:
			url = f"{self.api_url}ping?key={self.key}"
		else:
			url = f"{self.api_url}validate?key={self.key}"
		data = {
			"key": self.key,
			'mac': get_mac_address()
		}
		extraData = {"game": "bombcrypto", "name": self.instance_name}
		ret = curl(url, data, "POST", public_key=self.bot_rsa_public, private_key=self.key_crypt, extraData=extraData)

		if not ret['status']:
			if ping:
				self.ping_errors +=1
				if self.ping_errors <= 3:
					self.debug(self.lang.messages['error_connection'].replace("#", str(self.ping_errors)), "ERROR")
					return True
			if ret['msg'] in self.lang.messages:
				ret[msg] = self.lang.messages[ret['msg']]
			self.debug(f"{self.lang.messages['error_code']} #{ret['code']}: {ret['msg']}", self.lang.messages['error'].upper())
			return False
		else:
			self.pro = ret['result']['pro']
			ping_errors = 0
			if not ping:
				tmp = self.lang.messages['account_valid'].replace("X", str(ret['result']['instances'])).replace("Y", str(ret['result']['until']))
				self.debug(tmp)
		return True

	def ping_pong(self):
		return self.validate(True)

	def get_crypt_key(self, key):
		middle = int(len(key)/2)
		tmp1 = key[0:middle][::-1]
		tmp2 = key[middle:len(key)][::-1]
		return tmp2 + tmp1

	def decode_string(self, string):
		return self.get_crypt_key(base64.b64decode(self.get_crypt_key(string)).decode("utf-8"))

	def load_lang(self):
		module_path = f"langs.{self.lang_sel}"
		module = __import__(module_path, fromlist=["*"])
		lang = getattr(module, "Langs")
		return lang()

	def start_game(self):
		self.chrome.get("https://app.bombcrypto.io")
		wait_ready_state_completed(self.chrome)

		self.chrome.execute_script(f"document.querySelector('html').innerHTML = document.querySelector('iframe[title=Bombcrypto]').outerHTML; return true;")
		self.chrome.execute_script(f"document.title = '{self.instance_name}'; return true;")
		self.chrome.execute_script(f"document.querySelector('html').style.margin = 0; document.querySelector('html').style.padding = 0;")
		self.chrome.execute_script(f"document.querySelector('body').style.margin = 0; document.querySelector('body').style.padding = 0;")

		# Go inside the frame
		iframe = self.chrome.find_element_by_xpath('//iframe')
		self.chrome.switch_to.frame(iframe)

		self.chrome.execute_script(f"document.getElementById('unity-container').style.setProperty('left', 0); document.getElementById('unity-container').style.setProperty('right', 0); document.getElementById('unity-container').style.setProperty('top', 0); document.getElementById('unity-container').style.setProperty('transform', 'none');document.getElementById('unity-footer').remove();document.title = '{self.instance_name}'; return true;")

		# Check for terms
		test = self.wait_for_images(["./images/checkbox_terms.png", "./images/connect_button.png"], self.wait_loading)
		if not test:
			return False

		if test['key'] == 0:
			loc_checkbox = {
				"x": 237,
				"y": 407,
				"w": 30,
				"h": 30
			}
			self.click_on_location(loc_checkbox)
			sleep(1)

			loc_btn = {
				"x": 403,
				"y": 469,
				"w": 150,
				"h": 50
			}
			self.click_on_location(loc_btn)
			sleep(1)

		return self.connect_wallet()

	def unlock_wallet(self):
		self.chrome.get(f"chrome-extension://{self.metamask_extension_id}/home.html")
		wait_ready_state_completed(self.chrome)
		if wait_for_element_by_xpath(self.chrome, '//input[@id="password"]'):

			if self.metamask_pass:
				elem = self.chrome.find_element_by_xpath('//input[@id="password"]')
				elem.click()
				sleep(0.25)
				elem.send_keys(self.metamask_pass)
				sleep(0.25)
				self.chrome.find_element_by_xpath('//button[@role="button"]').click()
			else:
				self.debug(self.lang.messages['waiting_bnb_symbol'])

			if wait_for_element_by_xpath(self.chrome, '//img[contains(@src, "bnb.png")]', self.wait_loading):
				self.wallet_unlocked = True
				return True
		return False

	def connect_wallet(self):
		loc = self.wait_for_image("./images/connect_button.png", self.wait_loading)
		if loc:
			self.click_on_location(loc)
			
			# New login system
			if (self.username and self.password):
				sleep(2)
				loc_username = {"x": 377,"y": 199,"w": 225,"h": 27}
				loc_password = {"x": 377,"y": 243,"w": 225,"h": 27}
				loc_loginbtn = {"x": 420,"y": 310,"w": 120,"h": 34}

				self.click_on_location(loc_username)
				sleep(0.25)
				ActionChains(self.chrome).send_keys(self.username).perform()
				sleep(0.25)

				self.click_on_location(loc_password)
				sleep(0.25)
				ActionChains(self.chrome).send_keys(self.password).perform()
				sleep(0.25)

				self.click_on_location(loc_loginbtn)
				sleep(0.25)

				test = self.wait_for_image("./images/btn_ok.png", 2)
				if test:
					self.click_on_location(test)
			else:
				loc_btn = self.wait_for_image("./images/btn_login_metamask.png", 10)
				if loc_btn:
					sleep(1)
					self.click_on_location(loc_btn)
					self.debug(self.lang.messages['connecting_wallet'])

					if not self.wait_sign_request():
						return False

			test = self.wait_for_images(["./images/bau_header.png", "./images/error_bar.png"], 60)
			# If didn't found the login confirmation or found error_bar image at screen, needs to restart!
			if not test or ("key" in test and test['key'] == 1):
				self.debug(self.lang.messages['something_wrong'])
				return False
			self.wallet_connected = True
			return True
		return False

	def play(self):
		try:
			while True:
				sleep(0.25)
				if (self.last_ping_pong + 60) < time.time():
					test = self.ping_pong()
					if test:
						self.last_ping_pong = time.time()
					else:
						self.debug(self.lang.messages['lost_connection'], self.lang.messages['error'])
						self.quit()

				if self.detect_error():
					self.restart()

				self.do_bomb_stuff()

				sleep(1)
			return False
		except Exception as e:
			if self.debugVar:
				print("EXCEPTION: ")
				print(e)
				if self.debugVar == 2:
					traceback.print_exc()
			sleep(3)
			return False

	def get_screenshot(self, tries=0):
		if tries >= 3:
			return False
		try:
			imBytes = self.chrome.find_element_by_id('unity-canvas').screenshot_as_png
			im = Image.open(io.BytesIO(imBytes))
			im = im.convert('RGB')
			im = np.array(im)
			im = im[:, :, ::-1].copy()
			return im
		except:
			return self.get_screenshot((tries+1))

	def detect_error(self):
		# Take a single frame to work
		frame = self.get_screenshot()

		if self.locate_on_image("./images/loading_logo.png", frame):
			if not self.loading_detected:
				self.loading_detected = time.time()
			else:
				if (self.loading_detected + 60) > time.time():
					self.debug(self.lang.messages['error_loading_stuck'], self.lang.messages['error'])
					return True

		if self.locate_on_image("./images/error_bar.png", frame, confidence=0.9):
			self.debug(self.lang.messages['error_bar'])
			return True

		if not self.fixPathfind():
			self.debug(self.lang.messages['error_renewing_pathfind'])
			return True

		if self.wallet_unlocked and self.wallet_connected and self.able_to_work:
			if self.wait_for_image("./images/connect_button.png", 2):
				self.debug(self.lang.messages['error_login_restarted'])
				return True

		return False

	def fixPathfind(self):
		if self.last_pathfind and self.last_pathfind + (60 * self.pathfind_renew_interval) <= time.time():
			# Detects if its already "playing", if so: go back to main menu
			if self.locate_and_click("./images/btn_back.png", 3):
				if self.locate_and_click("./images/btn_treasure.png", 3):
					self.last_pathfind = time.time()
					return True
			return False
		return True

	def chest_check(self):
		sleep(1)
		chest = self.locate_on_image("./images/bau_header.png", self.get_screenshot())
		if chest:
			close = {
				'x': chest['x']-104, # +6 do offset do bau novo
				'y': chest['y']+94, # +6 do offset do bau novo
				'w':38,
				'h':38
			}
			self.click_on_location(chest)
			sleep(2)
			chest_ret, bcoin, heros = get_chest_screenshots(chest, self.get_screenshot())
			if chest_ret:
				self.send_chest(bcoin, heros)
			sleep(2)
			self.click_on_location(close)
		return True

	def locate_on_image(self, img_search, img_source=False, confidence=0.9, multi=False):
		if isinstance(img_source, (list, tuple, np.ndarray, str)):
			if isinstance(img_source, str):
				source = cv2.imread(img_source)
			else:
				source = img_source
		else:
			source = self.get_screenshot()

		search = cv2.imread(img_search)
		w, h = search.shape[:-1]

		try:
			res = cv2.matchTemplate(source, search, cv2.TM_CCOEFF_NORMED)
			loc = np.where(res >= confidence)
		except:
			return False

		if not len(loc):
			return False

		locs = []
		for pt in zip(*loc[::-1]):
			if multi:
				locs.append({"x": pt[0], "y": pt[1], "w": h, "h": w})
			else:
				locs = {"x": pt[0], "y": pt[1], "w": h, "h": w}
		return locs;

	def send_map(self):
		map_ss = self.get_screenshot()
		retval, buffer = cv2.imencode('.png', map_ss)
		base64img = base64.b64encode(buffer)
		url = f"{self.api_url}new_map?key={self.key}"
		data = {
			"key": self.key,
			'mac': get_mac_address(),
		}
		extra = {
			"img64": base64img.decode("utf-8"),
			'name': self.instance_name,
			'game': 'bombcrypto'
		}

		ret = curl(url, data, "POST", public_key=self.bot_rsa_public, private_key=self.key_crypt, extraData=extra)
		return ret['status']

	def send_chest(self, bcoins, bheros):
		retval, buffer = cv2.imencode('.png', bcoins)
		base64img1 = base64.b64encode(buffer)

		retval2, buffer2 = cv2.imencode('.png', bheros)
		base64img2 = base64.b64encode(buffer2)

		url = f"{self.api_url}chest?key={self.key}"
		data = {
			"key": self.key,
			'mac': get_mac_address()
		}
		extra = {
			"bcoins": base64img1.decode("utf-8"),
			"bheros": base64img2.decode("utf-8"),
			'name': self.instance_name,
			'game': 'bombcrypto'
		}
		ret = curl(url, data, "POST", public_key=self.bot_rsa_public, private_key=self.key_crypt, extraData=extra)
		return ret['status']

	def do_bomb_stuff(self):
		# Check if hero's are already working
		if self.start_work:
			if self.locate_and_click("./images/new_map.png", 1):
				self.debug(self.lang.messages['new_map'])
				sleep(3)
				if self.pro:
					self.send_map()
				self.maps_passed += 1
				# Trigger chest to update instance balance
				self.last_chest_check = 0

			# Random click on the top chest
			if self.pro:
				if self.last_chest_check + (60*self.chest_delay_rand) < time.time():
					self.chest_check()
					self.chest_delay_rand = random.randint(math.floor(self.chest_delay*0.75), self.chest_delay)
					self.last_chest_check = time.time()

			if self.maps_passed >= self.hero_test_after_maps:
				if not self.put_to_work():
					self.debug(self.lang.messages['error_loading_hero_list'])
					return self.wait_ready()
				self.maps_passed = 0
				self.hero_test_random = random.randint(math.floor(self.hero_test_after_mins*0.75), self.hero_test_after_mins)

			if (self.last_hero_check + (60 * self.hero_test_random)) < time.time():
				if not self.put_to_work():
					self.debug(self.lang.messages['error_loading_hero_list'])
					return self.wait_ready()
				self.maps_passed = 0
				self.hero_test_random = random.randint(math.floor(self.hero_test_after_mins*0.75), self.hero_test_after_mins)

			return True
		else:
			if not self.put_to_work():
				self.debug(self.lang.messages['error_loading_hero_list'])
				return self.wait_ready()
		return False

	def wait_ready(self):
		self.restart()
		images = ["./images/connect_button.png"]

		# Fix to find network error
		if self.unlock_wallet:
			images.append("./images/error_bar.png")

		if self.wait_for_images(images, 60):
			self.debug(self.lang.messages['page_loaded_bot_ready'])
			return True
		
		self.debug(self.lang.messages['page_didnt_load'])
		return False

	def put_to_work(self):
		# Detects if its already "playing", if so: go back to main menu
		self.locate_and_click("./images/btn_back.png", 2)

		if not self.locate_and_click("./images/btn_hero.png", 5):
			self.debug(self.lang.messages['error_loading_hero_list'])
			return self.wait_ready()

		test = self.wait_for_images(["./images/state_resting.png", "./images/state_working.png"], 60, confidence=0.95)
		if not test:
			self.debug(self.lang.messages['error_loading_hero_list'])
			return self.wait_ready()

		self.debug("Collection heroes data to send work")
		heroes = self.get_heroes()
		# print(heroes)

		if len(heroes):
			btns_sizes = {"w": 40, "h": 10}
			btns_work = [
				{"x": 381, "y": 194},
				{"x": 381, "y": 266},
				{"x": 381, "y": 338},
				{"x": 381, "y": 410},
				{"x": 381, "y": 482}
			]
			btns_rest = [
				{"x": 440, "y": 194},
				{"x": 440, "y": 266},
				{"x": 440, "y": 338},
				{"x": 440, "y": 410},
				{"x": 440, "y": 482}
			]
			btns_home = [
				{"x": 500, "y": 194},
				{"x": 500, "y": 266},
				{"x": 500, "y": 338},
				{"x": 500, "y": 410},
				{"x": 500, "y": 482}
			]

			working = 0
			resting = 0
			at_home = 0

			for test in heroes:
				if test['active']:
					working +=1
				else:
					if test['at_home']:
						at_home +=1
					else:
						resting +=1
			
			tot_heroes = len(heroes)

			# print(f"Total heroes: {tot_heroes}")
			# print(f"Working: {working}")
			# print(f"Resting: {resting}")
			# print(f"Resting at home: {at_home}")

			checks = 0
			ended = False

			while not ended:
				tmp_checks = 0

				minRange = 4 if self.account_heroes >= 5 else (self.account_heroes - 1)

				sentWork = 0
				for x in range(minRange, -1, -1):
					tmp_checks+=1
					actual_index = (tot_heroes-1)-checks-x
					if actual_index < 0:
						# print("Break 1")
						ended = True
						break

					hero = heroes[actual_index]

					# print(f"Checking index: {actual_index} [{checks}] {x}")
					# print(hero)

					if hero['active']:
						ended = True
						continue

					if hero['stam'] >= self.min_stam:
						loc_btn = {
							'x': btns_work[(4-x)]['x'],
							'y': btns_work[(4-x)]['y'],
							'w': btns_sizes['w'],
							'h': btns_sizes['h']
						}
						sleep(0.15)
						self.click_on_location(loc_btn)
						hero['active'] = True
						
						if hero['at_home']:
							at_home -=1
							hero['at_home'] = False
						else:
							resting -= 1

						working += 1
						sentWork +=1

				if not self.test_empty_bar():
					self.debug("Something went wrong while sending heroes to work, restarting")
					return self.wait_ready()

				if sentWork < 5:
					self.wheel_element2(self.chrome.find_element_by_id('unity-canvas'), -1, (4 * (5 - sentWork)))

				checks+=tmp_checks

		if self.use_house:
			sleep(1)
			self.check_house()

		sleep(1)
		self.last_hero_check = time.time()

		if not self.locate_and_click("./images/btn_close.png"):
			self.debug(self.lang.messages['error_loading_hero_list'])
			return self.wait_ready()

		if self.locate_and_click("./images/btn_treasure.png", 10):
			self.debug(self.lang.messages['working'])
			self.start_work = time.time()
			self.last_pathfind = time.time()
			self.last_chest_check = time.time()
			return True

		return False

	def test_empty_bar(self, timeout=15):
		start = time.time()
		emptyBarTest = ['test_empty_bar']
		while len(emptyBarTest) > 0:
			if start+timeout < time.time():
				return False
			sleep(0.25)
			emptyBarTest = self.locate_on_image('./images/empty_bar.png', self.get_screenshot())
		return True

	def send_home_update_index(self, heroes, hero):
		ret = []
		for tmp in heroes:
			if tmp['index'] > hero['index']:
				tmp['index'] -= 1
			ret.append(tmp)

		hero['index'] = len(ret)
		ret.append(hero)
		return ret

	def check_house(self):
		self.debug("Collection heroes data to test house")
		self.wheel_element2(self.chrome.find_element_by_id('unity-canvas'), -1, 40)
		sleep(1)

		heroes = sorted(self.get_heroes(), key=lambda d: d['stam'])

		# if self.debugVar == 2:
			# self.debug("Collected heroes list: " + json.dumps(heroes), "DEBUG")

		btns_sizes = {"w": 20, "h": 5}
		btns_home = [
			{"x": 510, "y": (194+5)},
			{"x": 510, "y": (266+5)},
			{"x": 510, "y": (338+5)},
			{"x": 510, "y": (410+5)},
			{"x": 510, "y": (482+5)}
		]

		while True:
			if len(heroes) == 0:
				if self.debugVar == 2:
					self.debug("List ended", "DEBUG")
				break

			hero = heroes.pop(0)

			if self.debugVar == 2:
				self.debug("Testing heroe: " + json.dumps(hero), "DEBUG")

			if hero['at_home']:
				if self.debugVar == 2:
					self.debug("At home, skiping", "DEBUG")
				continue

			self.wheel_element2(self.chrome.find_element_by_id('unity-canvas'), -1, 40)
			sleep(1)

			xxx = self.locate_on_image("./images/btn_home_disabled.png", self.get_screenshot(), confidence=0.85)
			if xxx:
				if self.debugVar == 2:
					self.debug("House is full, skiping", "DEBUG")
				break

			if (hero['index'] > 4):
				if self.debugVar == 2:
					self.debug("House not visible, scrolling down", "DEBUG")

				scroll = (hero['index']-4)
				# for x in range(0, scroll):
				# 	self.wheel_element(self.chrome.find_element_by_id('unity-canvas'), 1, 4)
				self.wheel_element(self.chrome.find_element_by_id('unity-canvas'), 1, (scroll*4))
				sleep(0.25)
				pos = 4
			else:
				pos = hero['index']

			loc_btn = {
				'x': btns_home[pos]['x'],
				'y': btns_home[pos]['y'],
				'w': btns_sizes['w'],
				'h': btns_sizes['h']
			}

			self.click_on_location(loc_btn)
			if self.debugVar == 2:
				self.debug(f"Sending hero at position #{pos} to work", "DEBUG")

			if not self.test_empty_bar():
				self.debug("Something went wrong while sending heroes to house, restarting")
				return self.wait_ready()

			hero['active'] = False
			hero['at_home'] = True
			hero['resting'] = False
			heroes = self.send_home_update_index(heroes, hero)

		return True

	def get_heroes(self):
		heroes = []
		time_start = time.time()
		while len(heroes) < self.account_heroes:
			if (time_start+self.wait_loading < time.time()):
				self.debug(f"Error searching heroes info, does your account have {self.account_heroes}? Check it into config.cfg")
				break
			
			sleep(1)

			frame = self.get_screenshot()

			buttons_work_active = self.locate_on_image("./images/state_working.png", frame, multi=True)
			tot_buttons_work_active = len(buttons_work_active)

			buttons_work_inactive = self.locate_on_image("./images/state_resting.png", frame, multi=True)
			tot_buttons_work_inactive = len(buttons_work_inactive)

			tot_found = tot_buttons_work_active+tot_buttons_work_inactive
			tot_heroes_before = len(heroes)

			# print(f"Total found {tot_found}")
			# print(f"Total tot_buttons_work_active {tot_buttons_work_active}")
			# print(f"Total tot_buttons_work_inactive {tot_buttons_work_inactive}")

			buttons = buttons_work_active
			for tmp in buttons_work_inactive:
				buttons.append(tmp)

			buttons = sorted(buttons, key=lambda d: d['y'])

			for button_work in buttons:
			# for button_work in buttons_work_active+buttons_work_inactive:
				offset = [button_work['x']-114, button_work['y']+19]
				size = [100, 11]
				
				stam_bar = frame[offset[1]:offset[1]+size[1], offset[0]:offset[0]+size[0]]
				stam = detect_stam(6, stam_bar)

				# cv2.imshow(f"stam {len(heroes)} = {stam}", stam_bar)

				btn_work_color = frame[button_work['y']+6][button_work['x']+6]
				at_house = False
				
				if self.use_house:
					btn_house_color = frame[button_work['y']+6][button_work['x']+125]
					at_house = True if btn_house_color[2] > 200 else False

				tmp = {
					'index': len(heroes),
					"stam": stam,
					'active': True if btn_work_color[1] > 150 else False,
					'at_home': at_house
				}

				# print(tmp)
				heroes.append(tmp)
			
			if len(heroes) != self.account_heroes:
				self.wheel_element(self.chrome.find_element_by_id('unity-canvas'), 1, 4 * tot_found)
				sleep(1)
		
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

		return heroes

	def wait_sign_request(self, delay=60):
		start = time.time()

		bombTab = False
		metamaskTab = False
		found = False

		while not found:
			sleep(1)
			if time.time() > start + delay:
				return False
			for handle in self.chrome.window_handles:
				self.chrome.switch_to.window(handle)
				if self.metamask_extension_id in self.chrome.current_url and '/signature-request' in self.chrome.current_url:
					metamaskTab = handle
				if 'app.bombcrypto.io' in self.chrome.current_url:
					bombTab = handle
				if metamaskTab and bombTab:
					found = True

		self.chrome.switch_to.window(metamaskTab)
		if wait_for_element_by_xpath(self.chrome, '//button[contains(@class, "request-signature__footer__sign-button")]'):
			self.chrome.find_element_by_xpath('//button[contains(@class, "request-signature__footer__sign-button")]').click()
			self.chrome.switch_to.window(bombTab)
			return True
		return False

	def wait_for_image(self, img_search, timeout=60, confidence = 0.9):
		start = time.time()
		loc = False
		while not loc:
			sleep(1)
			im = self.get_screenshot()
			loc = self.locate_on_image(img_search, im, confidence)
			if time.time() - start > timeout:
				break
		return loc

	def wait_for_images(self, searchImages = [], timeout = 60, confidence = 0.9):
		start = time.time()
		loc = None
		loc_key = None
		while not loc:
			sleep(1)
			frame = self.get_screenshot()

			for key,val in enumerate(searchImages):
				loc = self.locate_on_image(val, frame, confidence=0.9)
				if loc:
					loc_key = key
					break
				if (time.time() - start) > timeout:
					return False
				time.sleep(0.25)
		return {
			"loc": loc,
			"key": loc_key
		}

	def click_on_location(self, loc, offset = False, delay=False):
		if not offset:
			offset = {
				"w": math.floor(random.randint(math.floor(loc['w']*0.25), math.floor(loc['w']*0.75))),
				"h": math.floor(random.randint(math.floor(loc['h']*0.25), math.floor(loc['h']*0.75)))
			}
		ActionChains(self.chrome).move_to_element_with_offset(self.chrome.find_element_by_id('unity-canvas'), loc['x'] + offset['w'], loc['y'] + offset['h']).click().perform()
		return True

	def wheel_element(self, element, deltaY = 120, events = 1):
		error = element._parent.execute_script("""
			var element = arguments[0];
			var deltaY = arguments[1];
			var events = arguments[2];
			var box = element.getBoundingClientRect();
			var clientX = box.left + (box.width / 2);
			var clientY = box.top + (box.height / 2);
			var target = element.ownerDocument.elementFromPoint(clientX, clientY);

			for (var e = target; e; e = e.parentElement) {
			  if (e === element) {
			    target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
			    target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
			    for (var x=0;x < events;x++){
			    	target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
			    }
			    return;
			  }
			}    
			return "Element is not interactable";
			""", element, deltaY, events)
		if error:
			raise WebDriverException(error)
		return True

	def wheel_element2(self, element, deltaY = 120, events = 1):
		error = element._parent.execute_script("""
			var element = arguments[0];
			var deltaY = arguments[1];
			var events = arguments[2];
			var box = element.getBoundingClientRect();
			var clientX = box.left + (box.width / 2);
			var clientY = box.top + (box.height / 2);
			var target = element.ownerDocument.elementFromPoint(clientX, clientY);

			for (var e = target; e; e = e.parentElement) {
			  if (e === element) {
			    target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
			    target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
			    for (var x=0;x < events;x++){
			    	target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: -1}));
			    }
			    return;
			  }
			}    
			return "Element is not interactable";
			""", element, deltaY, events)
		if error:
			raise WebDriverException(error)
		return True

	def locate_and_click(self, searchImage, timeout = 60, confidence = 0.9, offset = False, delay=False):
		loc = self.wait_for_image(searchImage, timeout, confidence)
		if loc:
			self.click_on_location(loc, offset, delay=delay)
			return True
		return False