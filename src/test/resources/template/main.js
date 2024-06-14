window.onload = function() {
    var canvases = document.querySelectorAll('canvas');
    canvases.forEach(function(canvas) {
        var featurePassedCount = canvas.getAttribute('data-passed');
        var featureFailedCount = canvas.getAttribute('data-failed');
        var featureSkippedCount = canvas.getAttribute('data-skipped');
        var featureName = canvas.getAttribute('data-feature-name');
        var ctx = canvas.getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Passed', 'Failed', 'Skipped'],
                datasets: [{
                    data: [featurePassedCount, featureFailedCount, featureSkippedCount],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',  // Color for 'Passed'
                        'rgba(255, 99, 132, 0.2)',  // Color for 'Failed'
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: "Scenarios"
                    }
                }
            },
        });
    });
}