// SHOW/HIDE USERS
function toUsers(){
    let Users = document.getElementById('Users');
    if (Users.style.display==='none'){
        Users.style.display='block';
    } else {
        Users.style.display='none';
    };
};

// SHOW/HIDE QUESTIONS
function toQuestions(){
    let Questions = document.getElementById('Questions');
    if (Questions.style.display==='none'){
        Questions.style.display='block';
    } else {
        Questions.style.display='none';
    };
};

// STATISTICS PLOTS
function plotChart(data, chartElement, chartType, xLabels, yTitle, chartTitle, myScales){
    let ctx = document.getElementById(chartElement).getContext('2d');
    let myChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: xLabels,
            datasets: [{
                label: yTitle,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            legend: {
                display: false
            },
            title: {
                display: true,
                text: chartTitle,
                fontColor: 'white'
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            if (myScales){
                scales: myScales
            }
        }
    });
};
