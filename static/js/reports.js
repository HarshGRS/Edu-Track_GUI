// Reports page JavaScript with Chart.js integration
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    setupExportFunctions();
});

function initializeCharts() {
    // Grade Distribution Chart
    const gradeCtx = document.getElementById('gradeChart');
    if (gradeCtx) {
        new Chart(gradeCtx, {
            type: 'doughnut',
            data: {
                labels: ['A+', 'A', 'B+', 'B', 'C', 'F'],
                datasets: [{
                    data: [
                        gradeCounts['A+'] || 0,
                        gradeCounts['A'] || 0,
                        gradeCounts['B+'] || 0,
                        gradeCounts['B'] || 0,
                        gradeCounts['C'] || 0,
                        gradeCounts['F'] || 0
                    ],
                    backgroundColor: [
                        '#10b981', // A+
                        '#059669', // A
                        '#f59e0b', // B+
                        '#d97706', // B
                        '#06b6d4', // C
                        '#ef4444'  // F
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true,
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    // Performance Chart
    const performanceCtx = document.getElementById('performanceChart');
    if (performanceCtx) {
        new Chart(performanceCtx, {
            type: 'bar',
            data: {
                labels: performanceData.labels,
                datasets: [{
                    label: 'Percentage',
                    data: performanceData.data,
                    backgroundColor: performanceData.data.map(score => {
                        if (score >= 90) return '#10b981';
                        if (score >= 80) return '#059669';
                        if (score >= 70) return '#f59e0b';
                        if (score >= 60) return '#d97706';
                        if (score >= 50) return '#06b6d4';
                        return '#ef4444';
                    }),
                    borderRadius: 4,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Score: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart',
                    delay: function(context) {
                        return context.dataIndex * 100;
                    }
                }
            }
        });
    }
}

function setupExportFunctions() {
    // Export functions are now handled by Flask routes
    // PDF Export: /export/pdf
    // Excel Export: /export/excel
    console.log('✓ Export functions ready. Click buttons to download.');
}

// Utility functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas ${getToastIcon(type)}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 10);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getToastIcon(type) {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return icons[type] || icons.info;
}

// Add chart container styles
const chartStyle = document.createElement('style');
chartStyle.textContent = `
    .chart-card canvas {
        max-height: 300px;
    }

    .toast {
        position: fixed;
        top: 20px;
        right: -300px;
        background: white;
        border-radius: 8px;
        padding: 15px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 10000;
        transition: all 0.3s ease;
        opacity: 0;
        transform: translateX(100%);
        max-width: 400px;
    }

    .toast-success { border-left: 4px solid #10b981; }
    .toast-error { border-left: 4px solid #ef4444; }
    .toast-warning { border-left: 4px solid #f59e0b; }
    .toast-info { border-left: 4px solid #06b6d4; }

    .toast i {
        font-size: 1.2rem;
    }

    .toast-success i { color: #10b981; }
    .toast-error i { color: #ef4444; }
    .toast-warning i { color: #f59e0b; }
    .toast-info i { color: #06b6d4; }

    .toast button {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        color: #6b7280;
        margin-left: auto;
    }
`;
document.head.appendChild(chartStyle);