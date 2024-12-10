totalPlayedData = false;
weeklyPlayedData = false;


// Load the Google Charts library
google.charts.load('current', {'packages': ['corechart']});
google.charts.setOnLoadCallback(drawCharts);

function drawCharts(year = false, startWeek = false, endWeek = false, skip = false) {
    year = year || new Date().getFullYear();
    startWeek = startWeek || 1;
    endWeek = endWeek || 52;


    if (skip) {
        changeYearAndWeek(year, startWeek, endWeek);
        drawTotalPlayedChart(totalPlayedData);
        drawWeeklyPlayedChart(weeklyPlayedData);
        return;
    }

    fetch('/dashboard/data?year=' + year + '&startWeek=' + startWeek + '&endWeek=' + endWeek)
        .then(response => response.json())
        .then(data => {
            changeYearAndWeek(year, startWeek, endWeek);
            $('.spinner-border.user').parent().addClass('d-none');
            $('.visually-hidden.user').removeClass('visually-hidden');
            if (data.totalPlayed.length === 0) {
                document.getElementById('total-played-chart').innerHTML = '<p class="text-center text-muted">No data available</p>';
            } else {
                document.getElementById('total-played-chart').innerHTML = '';

                totalPlayedData = data.totalPlayed;
                drawTotalPlayedChart(data.totalPlayed);
            }
            if (data.weeklyPlayed.length === 0) {
                document.getElementById('weekly-played-chart').innerHTML = '<p class="text-center text-muted">No data available</p>';
            } else {
                document.getElementById('weekly-played-chart').innerHTML = '';

                weeklyPlayedData = data.weeklyPlayed;
                drawWeeklyPlayedChart(data.weeklyPlayed);
            }

        });
}

// Pie Chart: Total Played Per Game
function drawTotalPlayedChart(totalPlayedData) {
    const chartData = [['Game', 'Total Time', {role: 'link'}]];
    totalPlayedData.forEach(item => {
        const url = '/games/' + item.app_id;
        chartData.push([item.game_name + ' (' + item.total_time + ' hours)', item.total_time, url]);
    });

    const data = google.visualization.arrayToDataTable(chartData);
    const options = {
        title: 'Total Played Time Per Game',
        pieHole: 0.4,
        backgroundColor: bgColor,
        legend: {position: 'right', maxLines: 3, textStyle: {color: textColor}},
        titleTextStyle: {color: textColor},
    };

    const chart = new google.visualization.PieChart(document.getElementById('total-played-chart'));

    google.visualization.events.addListener(chart, 'select', function () {
        const selection = chart.getSelection();
        if (selection.length > 0) {
            const row = selection[0].row;
            const link = data.getValue(row, 2); // Get the URL
            if (link) {
                window.location.href = link; // Redirect
            } else {
                console.warn("No link found for the selected row.");
            }
        }
    });

    google.visualization.events.addListener(chart, 'onmouseover', function () {
        document.getElementById('total-played-chart').style.cursor = 'pointer';
    });

    chart.draw(data, options);
}

// Bar Chart: Played Per Game Per Week
function drawWeeklyPlayedChart(playedPerWeekData) {
    const header = ['Week'];
    const gameUrls = {}; // To map game names to their respective URLs

    // Populate header and game URL mapping
    playedPerWeekData.forEach(item => {
        if (!header.includes(item.game_name)) {
            header.push(item.game_name);
            gameUrls[item.game_name] = `/games/${item.app_id}`; // Add game URL
        }
    });

    const weeklyData = {};

    playedPerWeekData.forEach(item => {
        const week = 'Week ' + item.week;
        if (!weeklyData[week]) {
            weeklyData[week] = {};
        }
        if (!weeklyData[week][item.game_name]) {
            weeklyData[week][item.game_name] = 0;
        }
        weeklyData[week][item.game_name] += Math.round(item.total_time);
    });

    const chartData = [header];

    Object.keys(weeklyData).forEach(week => {
        const row = [week]; // Start with the week
        header.slice(1).forEach(game => {
            row.push(weeklyData[week][game] || 0); // Add total time for the game or 0 if not played
        });
        chartData.push(row);
    });

    const data = google.visualization.arrayToDataTable(chartData);

    const options = {
        title: 'Played Time Per Game Per Week',
        xAxis: {title: 'Week'},
        yAxis: {title: 'Total Time'},
        hAxis: {
            title: 'Week',
            titleTextStyle: {color: lightTextColor},
            textColor: textColor
        },
        vAxis: {
            minValue: 0,
            title: 'Total Time',
            titleTextStyle: {color: lightTextColor},
            textColor: textColor
        },
        legend: {position: 'top', maxLines: 3, textStyle: {color: textColor}},
        isStacked: true,
        backgroundColor: bgColor,
        titleTextStyle: {color: textColor},
    };

    const chart = new google.visualization.ColumnChart(document.getElementById('weekly-played-chart'));

    // Add pointer cursor on hover
    google.visualization.events.addListener(chart, 'onmouseover', function () {
        document.getElementById('weekly-played-chart').style.cursor = 'pointer';
    });

    google.visualization.events.addListener(chart, 'onmouseout', function () {
        document.getElementById('weekly-played-chart').style.cursor = 'default';
    });

    // Add click behavior
    google.visualization.events.addListener(chart, 'select', function () {
        const selection = chart.getSelection();
        if (selection.length > 0) {
            const row = selection[0].row; // Get the selected row index
            const column = selection[0].column; // Get the selected column index

            if (column > 0) { // Ensure a game column is selected (not the 'Week' column)
                const game = header[column]; // Get the game name from the header
                const url = gameUrls[game]; // Get the URL for the selected game
                if (url) {
                    window.location.href = url; // Redirect to the game's URL
                }
            }
        }
    });

    chart.draw(data, options);
}


window.addEventListener('resize', function () {
    drawCharts(false, false, false, true);
});

function changeYearAndWeek(year, startWeek, endWeek) {
    $('.year').text(year);
    $('#startWeekText').text(startWeek);
    $('#endWeekText').text(endWeek);
}

const darkModeToggle = document.querySelector('#dark-mode-toggle');
darkModeToggle.addEventListener('change', () => {
    bgColor = darkModeToggle.checked ? '#212529' : '#f8f9fa';
    textColor = darkModeToggle.checked ? '#f8f9fa' : '#000';
    lightTextColor = darkModeToggle.checked ? '#f8f9fa' : '#959595';

    drawCharts(false, false, false, true);
    drawChartsFriends(false, false, false, true);
});
