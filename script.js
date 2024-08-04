// Load the datasets
Promise.all([
    d3.csv("SpotifyFeatures.csv"),
    d3.csv("songs_normalize.csv")
]).then(function([spotifyData, genreData]) {
    // Prepare the data
    const scenes = [
        {title: "Most Popular Artists", key: "popularity"},
        {title: "Popular Genres Over Time", key: "popularity"},
        {title: "Streams by Year and Country", key: "streams"}
    ];

    let currentSceneIndex = 0;
    let currentYear = 2000; // Default year for the scatterplot

    // Extract unique genres
    const genres = Array.from(new Set(spotifyData.map(d => d.genre)));
    genres.unshift("all");

    // Populate the genre dropdown
    const genreSelect = d3.select("#genre-select");
    genreSelect.selectAll("option")
        .data(genres)
        .enter()
        .append("option")
        .attr("value", d => d)
        .text(d => d);

    // Define the slider for the second scene
    const sliderContainer = d3.select("#slider-container");
    const filterContainer = d3.select("#filter-container");

    const streamData = [
        { country: "United States", streams: [ { year: 2014, value: 10 }, { year: 2015, value: 18 }, { year: 2016, value: 25 }, { year: 2017, value: 35 }, { year: 2018, value: 50 }, { year: 2019, value: 70 }, { year: 2020, value: 100 }, { year: 2021, value: 120 }, { year: 2022, value: 140 }, { year: 2023, value: 160 } ] },
        { country: "Brazil", streams: [ { year: 2014, value: 3 }, { year: 2015, value: 6 }, { year: 2016, value: 10 }, { year: 2017, value: 15 }, { year: 2018, value: 25 }, { year: 2019, value: 40 }, { year: 2020, value: 60 }, { year: 2021, value: 75 }, { year: 2022, value: 90 }, { year: 2023, value: 110 } ] },
        { country: "Mexico", streams: [ { year: 2014, value: 2 }, { year: 2015, value: 4 }, { year: 2016, value: 8 }, { year: 2017, value: 12 }, { year: 2018, value: 20 }, { year: 2019, value: 35 }, { year: 2020, value: 50 }, { year: 2021, value: 65 }, { year: 2022, value: 80 }, { year: 2023, value: 95 } ] },
        { country: "United Kingdom", streams: [ { year: 2014, value: 4 }, { year: 2015, value: 8 }, { year: 2016, value: 12 }, { year: 2017, value: 20 }, { year: 2018, value: 30 }, { year: 2019, value: 45 }, { year: 2020, value: 65 }, { year: 2021, value: 80 }, { year: 2022, value: 95 }, { year: 2023, value: 110 } ] },
        { country: "Germany", streams: [ { year: 2014, value: 3 }, { year: 2015, value: 6 }, { year: 2016, value: 10 }, { year: 2017, value: 15 }, { year: 2018, value: 25 }, { year: 2019, value: 40 }, { year: 2020, value: 55 }, { year: 2021, value: 70 }, { year: 2022, value: 85 }, { year: 2023, value: 100 } ] }
    ];

    const totalStreams = streamData[0].streams.map(yearData => {
        return {
            year: yearData.year,
            value: streamData.reduce((sum, country) => {
                const countryYear = country.streams.find(d => d.year === yearData.year);
                return sum + (countryYear ? countryYear.value : 0);
            }, 0)
        };
    });

    function updateScene(index) {
        const scene = scenes[index];
        const key = scene.key;
        d3.select("#scene").html("");  // Clear the previous scene

        if (index === 0) {
            sliderContainer.style("display", "none");
            filterContainer.classed("d-none", false);

            // Create the bar chart for the most popular artists
            const svg = d3.select("#scene").append("svg")
                .attr("width", "100%")
                .attr("height", "100%");

            svg.append("text")
                .attr("x", "50%")
                .attr("y", 50)
                .attr("text-anchor", "middle")
                .attr("font-size", "24px")
                .text(scene.title);

            const margin = {top: 60, right: 30, bottom: 90, left: 60};
            const width = 800 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;

            const chartGroup = svg.append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            const x = d3.scaleBand()
                .range([0, width])
                .padding(0.1);

            const y = d3.scaleLinear()
                .range([height, 0]);

            const tooltip = d3.select("#tooltip");

            function updateChart(genre) {
                let filteredData = spotifyData;
                if (genre !== "all") {
                    filteredData = spotifyData.filter(d => d.genre === genre);
                }

                const artistData = d3.rollup(filteredData, v => d3.mean(v, d => +d.popularity), d => d.artist_name);
                const sortedData = Array.from(artistData, ([artist, popularity]) => ({artist, popularity}))
                                        .sort((a, b) => b.popularity - a.popularity)
                                        .slice(0, 10);

                x.domain(sortedData.map(d => d.artist));
                y.domain([0, d3.max(sortedData, d => d.popularity)]);

                chartGroup.selectAll(".bar").remove();

                chartGroup.selectAll(".bar")
                    .data(sortedData)
                    .enter().append("rect")
                    .attr("class", "bar")
                    .attr("x", d => x(d.artist))
                    .attr("width", x.bandwidth())
                    .attr("y", d => y(d.popularity))
                    .attr("height", d => height - y(d.popularity))
                    .style("fill", "steelblue")
                    .on("mouseover", function(event, d) {
                        tooltip.classed("hidden", false)
                               .style("left", `${event.pageX + 5}px`)
                               .style("top", `${event.pageY - 28}px`)
                               .text(`${d.artist}: ${d.popularity.toFixed(2)} million streams`);
                    })
                    .on("mouseout", function() {
                        tooltip.classed("hidden", true);
                    });

                chartGroup.selectAll(".axis").remove();

                chartGroup.append("g")
                    .attr("class", "axis axis--x")
                    .attr("transform", `translate(0,${height})`)
                    .call(d3.axisBottom(x))
                    .selectAll("text")
                    .attr("transform", "rotate(-45)")
                    .style("text-anchor", "end");

                chartGroup.append("g")
                    .attr("class", "axis axis--y")
                    .call(d3.axisLeft(y));

                // Add X axis label
                chartGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("transform", `translate(${width / 2},${height + margin.bottom / 2 + 10})`)
                    .text("Artists");

                // Add Y axis label
                chartGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("transform", `translate(-${margin.left / 2},${height / 2})rotate(-90)`)
                    .text("Average Popularity (millions of streams)");
            }

            updateChart("all");

            genreSelect.on("change", function() {
                const selectedGenre = d3.select(this).property("value");
                updateChart(selectedGenre);
            });

        } else if (index === 1) {
            sliderContainer.style("display", "block");
            filterContainer.classed("d-none", true);

            // Create the bubble chart for popular genres over time
            const svg = d3.select("#scene").append("svg")
                .attr("width", "100%")
                .attr("height", "100%");

            svg.append("text")
                .attr("x", "50%")
                .attr("y", 50)
                .attr("text-anchor", "middle")
                .attr("font-size", "24px")
                .text(scene.title);

            const margin = {top: 60, right: 30, bottom: 90, left: 60};
            const width = 800 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;

            const chartGroup = svg.append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            const x = d3.scaleLinear()
                .range([0, width])
                .domain([2000, 2020]);

            const y = d3.scaleLinear()
                .range([height, 0]);

            const radius = d3.scaleSqrt()
                .range([2, 20]);

            const color = d3.scaleOrdinal(d3.schemeCategory10);

            const tooltip = d3.select("#tooltip");

            function updateBubbleChart(year) {
                const filteredData = genreData.filter(d => +d.year === year);

                const genrePopularity = d3.rollup(filteredData, v => d3.mean(v, d => +d.popularity), d => d.genre);
                const bubbleData = Array.from(genrePopularity, ([genre, popularity]) => ({genre, popularity}));

                y.domain([0, d3.max(bubbleData, d => d.popularity)]);
                radius.domain([0, d3.max(bubbleData, d => d.popularity)]);

                // Adjust x domain to space out genres
                const genreX = d3.scalePoint()
                    .domain(bubbleData.map(d => d.genre))
                    .range([margin.left, width - margin.right]);

                chartGroup.selectAll(".dot").remove();

                chartGroup.selectAll(".dot")
                    .data(bubbleData)
                    .enter().append("circle")
                    .attr("class", "dot")
                    .attr("cx", d => genreX(d.genre))
                    .attr("cy", d => y(d.popularity))
                    .attr("r", d => radius(d.popularity))
                    .style("fill", d => color(d.genre))
                    .on("mouseover", function(event, d) {
                        tooltip.classed("hidden", false)
                               .style("left", `${event.pageX + 5}px`)
                               .style("top", `${event.pageY - 28}px`)
                               .text(`${d.genre}: ${d.popularity.toFixed(2)}`);
                    })
                    .on("mouseout", function() {
                        tooltip.classed("hidden", true);
                    });

                chartGroup.selectAll(".axis").remove();

                chartGroup.append("g")
                    .attr("class", "axis axis--x")
                    .attr("transform", `translate(0,${height})`)
                    .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format("d")));

                chartGroup.append("g")
                    .attr("class", "axis axis--y")
                    .call(d3.axisLeft(y));

                // Add X axis label
                chartGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("transform", `translate(${width / 2},${height + margin.bottom / 2 + 10})`)
                    .text("Year");

                // Add Y axis label
                chartGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("transform", `translate(-${margin.left / 2},${height / 2})rotate(-90)`)
                    .text("Popularity (millions of streams)");
            }

            updateBubbleChart(currentYear);

            // Get the slider input element
            const slider = d3.select("#yearSlider");

            slider.on("input", function() {
                currentYear = +this.value;
                d3.select("#yearLabel").text(currentYear);
                updateBubbleChart(currentYear);
            });

        } else {
            // Third visualization (new)
            sliderContainer.style("display", "none");
            filterContainer.classed("d-none", false);

            const svg = d3.select("#scene").append("svg")
                .attr("width", "100%")
                .attr("height", "100%");

            svg.append("text")
                .attr("x", "50%")
                .attr("y", 50)
                .attr("text-anchor", "middle")
                .attr("font-size", "24px")
                .text(scene.title);

            const margin = {top: 60, right: 30, bottom: 60, left: 60};
            const width = 800 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;

            const chartGroup = svg.append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            const x = d3.scaleLinear()
                .domain([2014, 2023])
                .range([0, width]);

            const y = d3.scaleLinear()
                .range([height, 0]);

            const color = d3.scaleOrdinal(d3.schemeCategory10);

            const line = d3.line()
                .x(d => x(d.year))
                .y(d => y(d.value));

            const tooltip = d3.select("#tooltip");

            function updateChart(country) {
                let data;
                if (country === "All") {
                    data = [{country: "Total", streams: totalStreams}];
                } else {
                    data = [streamData.find(d => d.country === country)];
                }

                y.domain([0, d3.max(data[0].streams, d => d.value)]);

                chartGroup.selectAll(".line").remove();
                chartGroup.selectAll(".dot").remove();
                chartGroup.selectAll(".axis").remove();

                data.forEach(d => {
                    chartGroup.append("path")
                        .datum(d.streams)
                        .attr("class", "line")
                        .attr("d", line)
                        .attr("fill", "none")
                        .attr("stroke", color(d.country))
                        .attr("stroke-width", 2);
                });

                chartGroup.selectAll(".dot")
                    .data(data[0].streams)
                    .enter().append("circle")
                    .attr("class", "dot")
                    .attr("cx", d => x(d.year))
                    .attr("cy", d => y(d.value))
                    .attr("r", 5)
                    .attr("fill", color(data[0].country))
                    .on("mouseover", function(event, d) {
                        tooltip.classed("hidden", false)
                               .style("left", `${event.pageX + 5}px`)
                               .style("top", `${event.pageY - 28}px`)
                               .html(`${data[0].country}<br>${d.year}: ${d.value} million streams`);
                    })
                    .on("mouseout", function() {
                        tooltip.classed("hidden", true);
                    });

                chartGroup.append("g")
                    .attr("class", "axis axis--x")
                    .attr("transform", `translate(0,${height})`)
                    .call(d3.axisBottom(x).tickFormat(d3.format("d")));

                chartGroup.append("g")
                    .attr("class", "axis axis--y")
                    .call(d3.axisLeft(y));

                // Add X axis label
                chartGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("transform", `translate(${width / 2},${height + margin.bottom - 10})`)
                    .text("Year");

                // Add Y axis label
                chartGroup.append("text")
                    .attr("text-anchor", "middle")
                    .attr("transform", `translate(-${margin.left - 10},${height / 2})rotate(-90)`)
                    .text("Streams (millions)");
            }

            updateChart("All");

            // Create country dropdown
            const countrySelect = d3.select("#filter-container")
                .append("select")
                .attr("id", "country-select")
                .on("change", function() {
                    const selectedCountry = d3.select(this).property("value");
                    updateChart(selectedCountry);
                });

            countrySelect.selectAll("option")
                .data(["All"].concat(streamData.map(d => d.country)))
                .enter().append("option")
                .attr("value", d => d)
                .text(d => d);
        }
    }

    // Initialize the first scene
    updateScene(currentSceneIndex);

    // Event listeners for navigation buttons
    d3.select("#prev").on("click", function() {
        if (currentSceneIndex > 0) {
            currentSceneIndex--;
            updateScene(currentSceneIndex);
        }
    });

    d3.select("#next").on("click", function() {
        if (currentSceneIndex < scenes.length - 1) {
            currentSceneIndex++;
            updateScene(currentSceneIndex);
        }
    });

    // Event listener for start button
    d3.select("#start").on("click", function() {
        d3.select("#title-slide").classed("d-none", true);
        d3.select("#visualization").classed("d-none", false);
    });
});

