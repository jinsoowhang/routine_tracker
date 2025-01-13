{{ config(materialized='table') }}

WITH automotive AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%aaa ca%' THEN 'AAA'
			WHEN LOWER(supplier) LIKE '%five star express ca%' THEN 'Five Star Express Car'
			WHEN LOWER(supplier) LIKE '%fletcher jones motor ca%' THEN 'Fletcher Jones Motor Cars'
			WHEN LOWER(supplier) LIKE '%hyundai%' THEN 'Hyundai'
			WHEN LOWER(supplier) LIKE '%radiator depo%' THEN 'Radiator Depot'
			WHEN LOWER(supplier) LIKE '%two thumbs up express%' THEN 'Two Thumbs Up Express Car Wash'
			WHEN LOWER(supplier) LIKE '%wild water express%' THEN 'Wild Water Express Car Wash'
		ELSE NULL END AS parent_supplier,
		'Automotive' AS spend_category
	FROM {{ ref('stg__finance') }}
),

bills_utilities AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%adobe %' THEN 'Adobe'
			WHEN LOWER(supplier) LIKE '%dmv%' THEN 'DMV'
			WHEN LOWER(supplier) LIKE '%fountainvalleyutil%' THEN 'Fountain Valley Utilities'
			WHEN LOWER(supplier) LIKE '%geico%' THEN 'Geico'
			WHEN LOWER(supplier) LIKE '%hadley tow%' THEN 'Hadley Tow'
			WHEN LOWER(supplier) LIKE '%homewarrant%' THEN 'Home Warranty'
			WHEN LOWER(supplier) LIKE '%mesa water district%' THEN 'Mesa Water District'
			WHEN LOWER(supplier) LIKE '%netflix%' THEN 'Netflix'
			WHEN LOWER(supplier) LIKE '%so california edison%' THEN 'Southern California Edison'
			WHEN LOWER(supplier) LIKE 'spectrum%' THEN 'Spectrum'
			WHEN LOWER(supplier) LIKE '%tmobile%' THEN 'T-Mobile'
		ELSE NULL END AS parent_supplier,
		'Bills & Utilities' AS spend_category
	FROM {{ ref('stg__finance') }}
),

education AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%udemy%' THEN 'Udemy'
		ELSE NULL END AS parent_supplier,
		'Education' AS spend_category
	FROM {{ ref('stg__finance') }}
),

entertainment AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%amc%' THEN 'AMC'
			WHEN LOWER(supplier) LIKE '%axs%' THEN 'AXS'
			WHEN LOWER(supplier) LIKE '%crypto.com%' THEN 'Crypto.com'
			WHEN LOWER(supplier) LIKE '%disney%' THEN 'Disney'
			WHEN LOWER(supplier) LIKE '%eventbrite%' THEN 'Eventbrite'
			WHEN LOWER(supplier) LIKE '%fever usa%' THEN 'Fever USA'
			WHEN LOWER(supplier) LIKE '%gametime%' THEN 'Gametime'
			WHEN LOWER(supplier) LIKE '%indian wells%' THEN 'Indian Wells' 
			WHEN LOWER(supplier) LIKE '%oc fair%' OR LOWER(supplier) LIKE '%orange county fair%' THEN 'OC Fair'
			WHEN LOWER(supplier) LIKE '%seatgeek%' THEN 'SeatGeek'
			WHEN LOWER(supplier) LIKE '%sofi stadium%' THEN 'SoFi Stadium'
			WHEN LOWER(supplier) LIKE '%squid game: the trial%' THEN 'Squid Game: The Trial'
			WHEN LOWER(supplier) LIKE '%stubhub%' THEN 'Stubhub'
			WHEN LOWER(supplier) LIKE '%tech roast show%' THEN 'Tech Roast Show'
			WHEN LOWER(supplier) LIKE '%ticketmaster%' OR LOWER(supplier) LIKE '%tm *kevin%' THEN 'Ticketmaster'
			WHEN LOWER(supplier) LIKE '%tickpick%' THEN 'TickPick'
		ELSE NULL END AS parent_supplier,
		'Entertainment' AS spend_category
	FROM {{ ref('stg__finance') }}
),

fees_adjustments AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%annual fee%' THEN 'Annual Fee'
			WHEN LOWER(supplier) LIKE '%annual membership%' THEN 'Annual Membership Fee'
			WHEN LOWER(supplier) LIKE '%credit balance refund%' THEN 'Credit Balance Refund'
			WHEN LOWER(supplier) LIKE '%payment%' THEN 'Payment'
			WHEN LOWER(supplier) LIKE '%purchase interest%' THEN 'Purchase Interest'
			WHEN LOWER(supplier) LIKE '%returned check%' THEN 'Returned Check/Declined Transaction'
		ELSE NULL END AS parent_supplier,
		'Fees & Adjustments' AS spend_category
	FROM {{ ref('stg__finance') }}
),

food_drink AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%7-eleven%' THEN '7-Eleven'
			WHEN LOWER(supplier) LIKE '%85c bakery%' THEN '85C Bakery Cafe'
			WHEN LOWER(supplier) LIKE '%angelos burgers%' THEN 'Angelos Burgers'
			WHEN LOWER(supplier) LIKE '%ayce sushi%' THEN 'AYCE Sushi'
			WHEN LOWER(supplier) LIKE '%boudin sf%' THEN 'Boudin SF'
			WHEN LOWER(supplier) LIKE '%broken yolk%' THEN 'Broken Yolk Cafe'
			WHEN LOWER(supplier) LIKE '%cava%' THEN 'Cava'
			WHEN LOWER(supplier) LIKE '%cham soot gol%' THEN 'Cham Soot Gol'
			WHEN LOWER(supplier) LIKE '%chick-fil-a%' OR LOWER(supplier) LIKE '%chick fil a%' THEN 'Chick-fil-A'
			WHEN LOWER(supplier) LIKE '%chipotle%' THEN 'Chipotle'
			WHEN LOWER(supplier) LIKE '%ciao pizzeria bar%' THEN 'Ciao Pizzeria Bar'
			WHEN LOWER(supplier) LIKE '%confetti%' THEN 'Confetti Italian Ice & Custard'
			WHEN LOWER(supplier) LIKE '%daveshotchicken%' OR LOWER(supplier) LIKE '%daves hot%' THEN 'Daves Hot Chicken'
			WHEN LOWER(supplier) LIKE '%denny%' THEN 'Dennys'
			WHEN LOWER(supplier) LIKE '%doordash%' THEN 'DoorDash'
			WHEN LOWER(supplier) LIKE '%el pollo loco%' THEN 'El Pollo Loco'
			WHEN LOWER(supplier) LIKE '%gourmondo catering%' THEN 'Gourmondo Catering'
			WHEN LOWER(supplier) LIKE '%grubhub%' THEN 'Grubhub'
			WHEN LOWER(supplier) LIKE '%in n out%' OR LOWER(supplier) LIKE '%in-n-out%' THEN 'In N Out Burger'
			WHEN LOWER(supplier) LIKE '%mendocino farms%' THEN 'Mendocino Farms'
			WHEN LOWER(supplier) LIKE '%mcdonald%' THEN 'McDonalds'
			WHEN LOWER(supplier) LIKE '%nobu%' THEN 'Nobu Restaurants'
			WHEN LOWER(supplier) LIKE '%panda express%' THEN 'Panda Express'
			WHEN LOWER(supplier) LIKE '%sees candy%' OR LOWER(supplier) LIKE '%seecandy%' THEN 'Sees Candy'
			WHEN LOWER(supplier) LIKE '%starbucks%' THEN 'Starbucks'
			WHEN LOWER(supplier) LIKE '%stonefire grill%' THEN 'Stonefire Grill'
			WHEN LOWER(supplier) LIKE '%subway%' THEN 'Subway'
			WHEN LOWER(supplier) LIKE '%sushi nikkei%' THEN 'Sushi Nikkei'
			WHEN LOWER(supplier) LIKE '%sushi imari%' THEN 'Sushi Imari'
			WHEN LOWER(supplier) LIKE '%taco mes%' THEN 'Taco Mesa'
			WHEN LOWER(supplier) LIKE '%the boiling crab%' THEN 'The Boiling Crab'
			WHEN LOWER(supplier) LIKE '%the hangout%' THEN 'The Hangout Pleasant Hill'
			WHEN LOWER(supplier) LIKE '%tom''s watch bar%' THEN 'Tom''s Watch Bar'
			WHEN LOWER(supplier) LIKE '%uber eats%' THEN 'Uber Eats'
			WHEN LOWER(supplier) LIKE '%wang cho%' THEN 'Wang Cho BBQ'
			WHEN LOWER(supplier) LIKE '%wingstop%' THEN 'Wingstop'
			WHEN LOWER(supplier) LIKE '%yard house%' THEN 'Yard House'
		ELSE NULL END AS parent_supplier,
		'Food & Drink' AS spend_category
	FROM {{ ref('stg__finance') }}
),

gas AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%arco%' THEN 'Arco'
			WHEN LOWER(supplier) LIKE '%circle k%' THEN 'Circle K'
		ELSE NULL END AS parent_supplier,
		'Gas' AS spend_category
	FROM {{ ref('stg__finance') }}
),

gifts_donations AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%benevity%' THEN 'Benevity'
			WHEN LOWER(supplier) LIKE '%home church%' THEN 'Home Church'
			WHEN LOWER(supplier) LIKE '%int''l rescue committee%' THEN 'Int''l Rescue Committee'
			WHEN LOWER(supplier) LIKE '%pacific west association%' THEN 'Pacific West Association'
			WHEN LOWER(supplier) LIKE '%project hope alliance%' THEN 'Project Hope Alliance'
			WHEN LOWER(supplier) LIKE '%world relief%' THEN 'World Relief'
		ELSE NULL END AS parent_supplier,
		'Gifts & Donations' AS spend_category
	FROM {{ ref('stg__finance') }}
),

groceries AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%costco%' AND LOWER(supplier) NOT LIKE '%costcosta%' THEN 'Costco'
			WHEN LOWER(supplier) LIKE '%h mart%' THEN 'H Mart'
			WHEN LOWER(supplier) LIKE '%home chef%' THEN 'Home Chef'
			WHEN LOWER(supplier) LIKE '%northgate market%' THEN 'Northgate Market'
			WHEN LOWER(supplier) LIKE '%sams club%' THEN 'Sams Club'
			WHEN LOWER(supplier) LIKE '%stater bros%' OR LOWER(supplier) LIKE '%staterbros%' THEN 'Stater Bros'
			WHEN LOWER(supplier) LIKE '%super king m%' THEN 'Super King Market'
			WHEN LOWER(supplier) LIKE '%target%' THEN 'Target'
			WHEN LOWER(supplier) LIKE '%trader joe%' THEN 'Trader Joes'
			WHEN LOWER(supplier) LIKE '%vons%' THEN 'Vons'
			WHEN LOWER(supplier) LIKE '%walmart%' OR LOWER(supplier) LIKE '%wal-mart%' THEN ''
			WHEN LOWER(supplier) LIKE '%zion market%' THEN 'Zion Market'
		ELSE NULL END AS parent_supplier,
		'Groceries' AS spend_category
	FROM {{ ref('stg__finance') }}
),

health_wellness AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%24 hour fitness%' THEN '24 Hour Fitness'
			WHEN LOWER(supplier) LIKE '%classpass%' THEN 'ClassPass'
			WHEN LOWER(supplier) LIKE '%mesaverdegolf%' THEN 'Costa Mesa Golf Course'
			WHEN LOWER(supplier) LIKE '%top seed tenn%' THEN 'Costa Mesa Tennis Center'
			WHEN LOWER(supplier) LIKE '%cvs%' THEN 'CVS Pharmacy'
			WHEN LOWER(supplier) LIKE '%kaiser%' THEN 'Kaiser Permanente'
			WHEN LOWER(supplier) LIKE '%rite aid%' THEN 'Rite Aid'
			WHEN LOWER(supplier) LIKE '%honest oral surgeon%' THEN 'Honest Oral Surgeon'
			WHEN LOWER(supplier) LIKE '%hospital%' THEN 'Others - Hospital'
			WHEN LOWER(supplier) LIKE '%pharmacy%' THEN 'Others - Pharmacy'
			WHEN LOWER(supplier) LIKE '%spa%' THEN 'Spa'
			WHEN LOWER(supplier) LIKE '%walgreens%' THEN 'Walgreens'
		ELSE NULL END AS parent_supplier,
		'Health & Wellness' AS spend_category
	FROM {{ ref('stg__finance') }}
),

home AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%at home store%' THEN 'At Home'
			WHEN LOWER(supplier) LIKE '%home depot%' THEN 'Home Depot'
			WHEN LOWER(supplier) LIKE '%pest control%' THEN 'Pest Control'
			WHEN LOWER(supplier) LIKE '%plumbing%' THEN 'Plumbing'
			WHEN LOWER(supplier) LIKE '%u-haul%' THEN 'U-Haul'
		ELSE NULL END AS parent_supplier,
		'Home' AS spend_category
	FROM {{ ref('stg__finance') }}
),

personal AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%costa mesa animal%' THEN 'Costa Mesa Animal Hospital'
			WHEN LOWER(supplier) LIKE '%dhl%' THEN 'DHL'
			WHEN LOWER(supplier) LIKE '%the ups store%' THEN 'The UPS Store'
			WHEN LOWER(supplier) LIKE '%vca westcoast%' THEN 'VCA Animal Hospital'
			WHEN LOWER(supplier) LIKE '%warner avenue animal%' THEN 'Warner Avenue Animal Hospital'
		ELSE NULL END AS parent_supplier,
		'Personal' AS spend_category
	FROM {{ ref('stg__finance') }}
),

professional_services AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%intuit%' THEN 'Intuit'
			WHEN LOWER(supplier) LIKE '%supra%' THEN 'Supra'
		ELSE NULL END AS parent_supplier,
		'Professional Services' AS spend_category
	FROM {{ ref('stg__finance') }}
),

shopping AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%99-cents-only%' THEN '99 Cents Only'
			WHEN LOWER(supplier) LIKE '%adidas%' THEN 'Adidas'
			WHEN LOWER(supplier) LIKE '%amzn%' OR LOWER(supplier) LIKE '%amazon%' THEN 'Amazon'
			WHEN LOWER(supplier) LIKE '%bloomingdales%' THEN 'Bloomingdales'
			WHEN LOWER(supplier) LIKE '%calvin klein%' THEN 'Calvin Klein'
			WHEN LOWER(supplier) LIKE '%cettire%' THEN 'Cettire'
			WHEN LOWER(supplier) LIKE '%coach inc%' OR LOWER(supplier) LIKE '%coach outlet%' THEN 'Coach Inc'
			WHEN LOWER(supplier) LIKE '%dhgate%' THEN 'DHgate'
			WHEN LOWER(supplier) LIKE '%dollar tree%' THEN 'Dollar Tree'
			WHEN LOWER(supplier) LIKE '%duty free%' THEN 'Duty Free Shopping'
			WHEN LOWER(supplier) LIKE '%ebay%' THEN 'eBay'
			WHEN LOWER(supplier) LIKE '%forever 21%' THEN 'Forever 21'
			WHEN LOWER(supplier) LIKE '%hollister%' THEN 'Hollister Co'
			WHEN LOWER(supplier) LIKE '%kate spade%' THEN 'Kate Spade'
			WHEN LOWER(supplier) LIKE '%louis vuitton%' THEN 'Louis Vuitton'
			WHEN LOWER(supplier) LIKE '%marc jacobs%' THEN 'Marc Jacobs'
			WHEN LOWER(supplier) LIKE '%michael kors%' THEN 'Michael Kors'
			WHEN LOWER(supplier) LIKE '%nike%' THEN 'Nike'
			WHEN LOWER(supplier) LIKE '%nordrack%' OR LOWER(supplier) LIKE '%nordstrom%' THEN 'Nordstrom Rack'
			WHEN LOWER(supplier) LIKE '%offerup%' THEN 'OfferUp'
			WHEN LOWER(supplier) LIKE '%petco%' THEN 'Petco'
			WHEN LOWER(supplier) LIKE '%petsmart%' THEN 'Petsmart'
			WHEN LOWER(supplier) LIKE '%playstation network%' THEN 'Playstation'
			WHEN LOWER(supplier) LIKE '%ross%' THEN 'Ross Stores'
			WHEN LOWER(supplier) LIKE '%saks%' THEN 'Saks Fifth Avenue'
			WHEN LOWER(supplier) LIKE '%ssense%' THEN 'SSENSE'
			WHEN LOWER(supplier) LIKE '%tennis spectrum%' THEN 'Tennis Spectrum'
			WHEN LOWER(supplier) LIKE '%thefarmersdog%' THEN 'The Farmers Dog'
		ELSE NULL END AS parent_supplier,
		'Shopping' AS spend_category
	FROM {{ ref('stg__finance') }}
),

travel AS (
	SELECT DISTINCT
		supplier,
		CASE
			-- WHEN LOWER(supplier) LIKE '%%' THEN ''
			WHEN LOWER(supplier) LIKE '%405 express lanes%' THEN '405 Express Lanes'
			WHEN LOWER(supplier) LIKE '%airbnb%' THEN 'Airbnb'
			WHEN LOWER(supplier) LIKE '%avis%' THEN 'Avis Car Rental'
			WHEN LOWER(supplier) LIKE '%copa air%' THEN 'Copa Airlines'
			WHEN LOWER(supplier) LIKE '%courtyard%' THEN 'Courtyard by Marriott'
			WHEN LOWER(supplier) LIKE '%delta%' THEN 'Delta Airlines'
			WHEN LOWER(supplier) LIKE '%expedia%' THEN 'Expedia'
			WHEN LOWER(supplier) LIKE '%flightnetwrk%' THEN 'Flight Network'
			WHEN LOWER(supplier) LIKE '%four points by shera%' THEN 'Four Points by Sheraton'
			WHEN LOWER(supplier) LIKE '%gol linhas%' THEN 'GOL Linhas'
			WHEN LOWER(supplier) LIKE '%hotel adagio%' THEN 'Hotel Adagio'
			WHEN LOWER(supplier) LIKE '%jetblue%' THEN 'Jet Blue'
			WHEN LOWER(supplier) LIKE '%john wayne airport%' THEN 'John Wayne Airport'
			WHEN LOWER(supplier) LIKE '%lan airline%' THEN 'LAN Airlines'
			WHEN LOWER(supplier) LIKE '%luxor%' THEN 'Luxor Hotel & Casino'
			WHEN LOWER(supplier) LIKE '%lyft%' THEN 'Lyft'
			WHEN LOWER(supplier) LIKE '%marriott%' THEN 'Marriott Hotel'
			WHEN LOWER(supplier) LIKE '%metro expresslanes%' THEN 'Metro ExpressLanes'
			WHEN LOWER(supplier) LIKE '%oojocom%' THEN 'Oojo.com'
			WHEN LOWER(supplier) LIKE '%residence inn%' THEN 'Residence Inn'
			WHEN LOWER(supplier) LIKE '%signia%' THEN 'Signia by Hilton'
			WHEN LOWER(supplier) LIKE '%southwes%' OR LOWER(supplier) LIKE '%points rapid rewards%' THEN 'Southwest Airlines'
			WHEN LOWER(supplier) LIKE '%taca air%' THEN 'Taca Airlines'
			WHEN LOWER(supplier) LIKE '%towneplace suites%' THEN 'TownePlace Suites'
			WHEN LOWER(supplier) LIKE '%uber%' THEN 'Uber'
			WHEN LOWER(supplier) LIKE '%westin%' THEN 'Westin Hotel'
		ELSE NULL END AS parent_supplier,
		'Travel' AS spend_category
	FROM {{ ref('stg__finance') }}
),

results AS (
	SELECT * FROM automotive WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM bills_utilities WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM education WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM entertainment WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM fees_adjustments WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM food_drink WHERE parent_supplier IS NOT NULL
	UNION 
	SELECT * FROM gas WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM gifts_donations WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM groceries WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM health_wellness WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM home WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM personal WHERE parent_supplier IS NOT NULL
	UNION   
	SELECT * FROM professional_services WHERE parent_supplier IS NOT NULL
	UNION 
	SELECT * FROM shopping WHERE parent_supplier IS NOT NULL
	UNION  
	SELECT * FROM travel WHERE parent_supplier IS NOT NULL
)

SELECT *
FROM results