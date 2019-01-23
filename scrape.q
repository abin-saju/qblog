// Load embedPy
\l p.q

// Use european date format
\z 1

// Empty schema
hotelInfo:flip `t`destination`hotel`checkin`checkout`price!"pssddj"$\:();

system "mkdir -p db";

// Empty folder
system "l db";

// If table to store data doesn't exist, create it.
if[not `HotelInfo in .Q.pt;
	.Q.dd[hsym `$string .z.d;`HotelInfo`] set .Q.en[`:.] hotelInfo;
	system "l ."
	];

// Load definitions from the script
pyscript:.p.import[`hotelscrape];
.scrape.start:pyscript`:startUp;
.scrape.getData:pyscript`:enterDestAndScrape;

runProgram:{[hotelInfo]
	//Initialise some variables
	url:"https://samplesite.com";
	dest:("Rome, Italy"; "London, United Kingdom";  "Dublin, Ireland"; "New York, United States"; "Newry, United Kingdom");
	chkin:"23/01/2019";
	chkout:"25/01/2019";

	driver:.scrape.start[]`;

	scrapeData:{[url;driver;dest;chkin;chkout]
		data:.scrape.getData[url;driver;dest;chkin;chkout]`;
		:([] t:.z.p; destination:`$dest; hotel:`$data[0]; checkin:"D"$chkin; checkout:"D"$chkout; price:"J"$data[1])
		};

	data:raze scrapeData[url;driver;;chkin;chkout] each dest;

	if[count data;.Q.dd[hsym (`$string .z.d);`HotelInfo`] upsert .Q.en[`:.] upsert[hotelInfo;data];system "l ."]
	}