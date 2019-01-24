// Load embedPy
\l p.q

// Use European date format
\z 1

//Create folder if it doesn't exist
system "mkdir -p db";

// Empty folder if running the first time
\l db;

// If table to store data doesn't exist, create it.
if[not `HotelInfo in .Q.pt;
	// Set down empty schema if table doesn't exist
	.Q.dd[hsym `$string .z.d;`HotelInfo`] set .Q.en[`:.] flip `t`destination`hotel`checkin`checkout`price!"pssddj"$\:();
	system "l ."
	];

// Load definitions from the python script
pyscript:.p.import[`hotelscrape];
.pyscrape.start:pyscript`:startUp;
.pyscrape.getData:pyscript`:enterDestAndScrape;

// Helper function to put data in the correct format
scrapeData:{[url;driver;dest;chkin;chkout]
	data:.pyscrape.getData[url;driver;dest;chkin;chkout]`;
	:([] t:.z.p; destination:`$dest; hotel:`$data[0]; checkin:"D"$chkin; checkout:"D"$chkout; price:"J"$data[1])
	};

runProgram:{[]
	// Initialise some variables
	url:"https://samplesite.com";
	dest:("Rome, Italy"; "London, United Kingdom";  "Dublin, Ireland"; "New York, United States"; "Newry, United Kingdom");
	chkin:"23/01/2019";
	chkout:"25/01/2019";

	// Start the session and scrape date from the url
	driver:.pyscrape.start[]`;
	data:raze scrapeData[url;driver;;chkin;chkout] each dest;

	// Upsert new data to on-disk table if any
	if[count data;.Q.dd[hsym (`$string .z.d);`HotelInfo`] upsert .Q.en[`:.] data;system "l ."]
	}
