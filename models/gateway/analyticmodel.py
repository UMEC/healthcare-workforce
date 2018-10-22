# Gateway to python analytic model. 
# NodeJS will invoke this gateway in order to execute the analytic model, and retrieve the resulting output.
import sys

response = { 
	"input_data" : sys.argv[1],
	"output_data" : [
	  {
		"_id": "5bce4e986afa79ecbf171be7",
		"index": 0,
		"guid": "d1810c42-31eb-4902-9e94-f582e76e681d",
		"isActive": 'true',
		"balance": "$2,301.69",
		"picture": "http://placehold.it/32x32",
		"age": 26,
		"eyeColor": "brown",
		"name": "Mullins Galloway",
		"gender": "male",
		"company": "ECLIPTO",
		"email": "mullinsgalloway@eclipto.com",
		"phone": "+1 (822) 450-3389",
		"address": "987 Highland Boulevard, Vivian, Federated States Of Micronesia, 7659",
		"about": "Et qui duis pariatur quis cillum sit qui. Veniam ea ea cupidatat laborum consequat commodo aute reprehenderit sint esse ipsum laborum. Cillum ad incididunt dolor quis. Amet proident qui exercitation dolor ut ullamco exercitation. Commodo id laborum culpa dolor.\r\n",
		"registered": "2015-12-17T01:16:26 +07:00",
		"latitude": -39.733556,
		"longitude": -20.272094,
		"tags": [
		  "duis",
		  "est",
		  "proident",
		  "non",
		  "dolor",
		  "aliqua",
		  "est"
		],
		"friends": [
		  {
			"id": 0,
			"name": "Lyons Carroll"
		  },
		  {
			"id": 1,
			"name": "Nichols Beard"
		  },
		  {
			"id": 2,
			"name": "Conway Leblanc"
		  }
		],
		"greeting": "Hello, Mullins Galloway! You have 10 unread messages.",
		"favoriteFruit": "banana"
	  },
	  {
		"_id": "5bce4e98ab82b55aa9d2afcb",
		"index": 1,
		"guid": "e377a745-6fc1-4a0d-ae65-3846e3bf2cfd",
		"isActive": 'false',
		"balance": "$3,040.74",
		"picture": "http://placehold.it/32x32",
		"age": 32,
		"eyeColor": "brown",
		"name": "Key Stewart",
		"gender": "male",
		"company": "ZENTILITY",
		"email": "keystewart@zentility.com",
		"phone": "+1 (831) 410-2899",
		"address": "331 Moore Street, Lutsen, Minnesota, 5570",
		"about": "Consequat voluptate minim adipisicing duis. Sint do cillum anim excepteur sint anim ea pariatur eiusmod ea exercitation. Cupidatat veniam esse consequat voluptate officia amet amet deserunt consequat deserunt est. Est nulla tempor mollit ex elit ex consectetur minim eiusmod commodo exercitation deserunt id.\r\n",
		"registered": "2014-02-25T10:31:34 +07:00",
		"latitude": -24.255414,
		"longitude": 6.466176,
		"tags": [
		  "nulla",
		  "ullamco",
		  "aliquip",
		  "laboris",
		  "magna",
		  "ad",
		  "sit"
		],
		"friends": [
		  {
			"id": 0,
			"name": "Gray Knowles"
		  },
		  {
			"id": 1,
			"name": "Lacy Dennis"
		  },
		  {
			"id": 2,
			"name": "Juliet Berry"
		  }
		],
		"greeting": "Hello, Key Stewart! You have 5 unread messages.",
		"favoriteFruit": "strawberry"
	  },
	  {
		"_id": "5bce4e98f7109efc67034950",
		"index": 2,
		"guid": "78b8c7ad-ee0b-4196-bf95-927e777c9dc0",
		"isActive": 'false',
		"balance": "$3,601.41",
		"picture": "http://placehold.it/32x32",
		"age": 28,
		"eyeColor": "blue",
		"name": "Essie Fuentes",
		"gender": "female",
		"company": "EBIDCO",
		"email": "essiefuentes@ebidco.com",
		"phone": "+1 (864) 437-3542",
		"address": "959 Cadman Plaza, Roy, South Carolina, 4790",
		"about": "Pariatur deserunt occaecat adipisicing irure ex non do pariatur. Qui cillum voluptate mollit sunt in minim labore incididunt sunt nulla. Nostrud esse minim dolore do ea dolore occaecat sint.\r\n",
		"registered": "2014-03-24T11:42:16 +06:00",
		"latitude": 76.438521,
		"longitude": 1.790111,
		"tags": [
		  "dolor",
		  "ullamco",
		  "nulla",
		  "esse",
		  "do",
		  "consequat",
		  "voluptate"
		],
		"friends": [
		  {
			"id": 0,
			"name": "Bowman Davis"
		  },
		  {
			"id": 1,
			"name": "Mandy Bush"
		  },
		  {
			"id": 2,
			"name": "Amy Bright"
		  }
		],
		"greeting": "Hello, Essie Fuentes! You have 9 unread messages.",
		"favoriteFruit": "strawberry"
	  },
	  {
		"_id": "5bce4e98bf1540f97d4536e4",
		"index": 3,
		"guid": "2be81ae0-4288-4ffc-8c34-ca47378da6cf",
		"isActive": 'true',
		"balance": "$2,084.79",
		"picture": "http://placehold.it/32x32",
		"age": 36,
		"eyeColor": "green",
		"name": "Johnnie Hutchinson",
		"gender": "female",
		"company": "OLYMPIX",
		"email": "johnniehutchinson@olympix.com",
		"phone": "+1 (838) 481-2394",
		"address": "955 Dwight Street, Boyd, Marshall Islands, 5390",
		"about": "Cillum tempor commodo excepteur nulla veniam dolor sunt consequat proident. Pariatur dolor excepteur anim laboris eiusmod cupidatat magna enim esse pariatur proident ullamco fugiat ipsum. Laborum occaecat cupidatat ipsum nulla occaecat. Quis magna occaecat laboris commodo veniam incididunt. Adipisicing ut amet est aliquip. Commodo exercitation dolore do anim aliqua veniam dolor sunt excepteur.\r\n",
		"registered": "2017-04-04T10:59:50 +06:00",
		"latitude": 50.685137,
		"longitude": 33.411934,
		"tags": [
		  "sit",
		  "elit",
		  "reprehenderit",
		  "esse",
		  "fugiat",
		  "ipsum",
		  "mollit"
		],
		"friends": [
		  {
			"id": 0,
			"name": "York Terrell"
		  },
		  {
			"id": 1,
			"name": "Jerry Dodson"
		  },
		  {
			"id": 2,
			"name": "Nanette Long"
		  }
		],
		"greeting": "Hello, Johnnie Hutchinson! You have 5 unread messages.",
		"favoriteFruit": "banana"
	  },
	  {
		"_id": "5bce4e985ad8ffb14a752958",
		"index": 4,
		"guid": "72d74bb5-bedf-4c3f-8e32-88d1991da0dc",
		"isActive": 'false',
		"balance": "$3,521.47",
		"picture": "http://placehold.it/32x32",
		"age": 22,
		"eyeColor": "green",
		"name": "Latisha Weber",
		"gender": "female",
		"company": "RODEMCO",
		"email": "latishaweber@rodemco.com",
		"phone": "+1 (875) 505-2218",
		"address": "370 Jodie Court, Homestead, Illinois, 1394",
		"about": "Aute anim anim duis ex cillum exercitation et minim occaecat qui elit dolor. Est mollit adipisicing consequat ullamco. Cillum velit labore cupidatat non ut deserunt deserunt aliqua esse. Proident mollit et anim fugiat ut laborum veniam cupidatat adipisicing. Cupidatat labore veniam id labore occaecat consequat laboris et do qui est voluptate consectetur.\r\n",
		"registered": "2016-04-12T01:10:03 +06:00",
		"latitude": 70.1336,
		"longitude": 140.775703,
		"tags": [
		  "duis",
		  "velit",
		  "irure",
		  "duis",
		  "magna",
		  "occaecat",
		  "ipsum"
		],
		"friends": [
		  {
			"id": 0,
			"name": "Whitfield Lindsay"
		  },
		  {
			"id": 1,
			"name": "Watkins Wise"
		  },
		  {
			"id": 2,
			"name": "Bolton Key"
		  }
		],
		"greeting": "Hello, Latisha Weber! You have 4 unread messages.",
		"favoriteFruit": "banana"
	  },
	  {
		"_id": "5bce4e98031c802dba2001cc",
		"index": 5,
		"guid": "2177145f-36c9-4ff4-b911-505b8e6cdeff",
		"isActive": 'false',
		"balance": "$1,651.80",
		"picture": "http://placehold.it/32x32",
		"age": 36,
		"eyeColor": "green",
		"name": "Stanton Allison",
		"gender": "male",
		"company": "ORBIN",
		"email": "stantonallison@orbin.com",
		"phone": "+1 (996) 402-2150",
		"address": "453 Knickerbocker Avenue, Jenkinsville, Wisconsin, 9160",
		"about": "Et irure aute aliquip consectetur elit ipsum eiusmod cupidatat enim est. Do fugiat sunt esse nostrud culpa excepteur. Exercitation velit voluptate ad occaecat eiusmod anim consectetur eiusmod amet laboris proident nostrud. Lorem eu ipsum incididunt eu fugiat exercitation nulla consequat culpa veniam aliquip ex. Tempor duis ut adipisicing sit voluptate enim anim labore eiusmod laborum esse excepteur. Id tempor duis consectetur ea voluptate laborum magna anim et. Anim ut esse adipisicing adipisicing incididunt qui.\r\n",
		"registered": "2016-11-22T11:23:52 +07:00",
		"latitude": 64.64409,
		"longitude": 170.042998,
		"tags": [
		  "nulla",
		  "cupidatat",
		  "sit",
		  "ad",
		  "ipsum",
		  "ipsum",
		  "nulla"
		],
		"friends": [
		  {
			"id": 0,
			"name": "Romero Rodgers"
		  },
		  {
			"id": 1,
			"name": "Reese Delacruz"
		  },
		  {
			"id": 2,
			"name": "Mcknight Kennedy"
		  }
		],
		"greeting": "Hello, Stanton Allison! You have 1 unread messages.",
		"favoriteFruit": "apple"
	  },
	  {
		"_id": "5bce4e98040dfabbc1bf64bd",
		"index": 6,
		"guid": "8bea8aa9-8400-4119-840f-0b83b154752a",
		"isActive": 'false',
		"balance": "$1,904.00",
		"picture": "http://placehold.it/32x32",
		"age": 24,
		"eyeColor": "blue",
		"name": "Holden Langley",
		"gender": "male",
		"company": "ZOGAK",
		"email": "holdenlangley@zogak.com",
		"phone": "+1 (927) 423-3094",
		"address": "922 Bryant Street, Hemlock, Oklahoma, 4138",
		"about": "Nulla duis Lorem et amet proident veniam id sit laboris irure do reprehenderit. Dolor labore proident anim deserunt laboris officia officia aliqua. Laborum ea culpa ex excepteur. Do pariatur labore aliqua nisi adipisicing nostrud nostrud irure exercitation labore aute. Aute deserunt sunt sunt id et quis qui culpa laboris minim laboris. Officia aliquip ex mollit proident elit est irure qui sunt amet consectetur mollit adipisicing.\r\n",
		"registered": "2014-09-10T10:59:56 +06:00",
		"latitude": 43.141908,
		"longitude": 99.863547,
		"tags": [
		  "dolore",
		  "reprehenderit",
		  "esse",
		  "consequat",
		  "voluptate",
		  "non",
		  "in"
		],
		"friends": [
		  {
			"id": 0,
			"name": "Rose Holland"
		  },
		  {
			"id": 1,
			"name": "Sondra Marquez"
		  },
		  {
			"id": 2,
			"name": "Ellis Andrews"
		  }
		],
		"greeting": "Hello, Holden Langley! You have 10 unread messages.",
		"favoriteFruit": "strawberry"
	  }
	]
}

print (response)