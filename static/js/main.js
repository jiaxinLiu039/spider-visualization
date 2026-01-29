document.addEventListener('DOMContentLoaded', function() {
    // 初始化图表
    const chartData = window.chartData;
    if (chartData) {
        try {
            console.log('开始初始化图表...');
            
            // 初始化所有图表
            const charts = [
                { id: 'chart1', data: chartData.graph1 },
                { id: 'chart2', data: chartData.graph2 },
                { id: 'chart3', data: chartData.graph3 },
                { id: 'chart4', data: chartData.graph4 },
                { id: 'chart5', data: chartData.graph5 }
            ];

            charts.forEach(chart => {
                if (chart.data && chart.data.data && chart.data.layout) {
                    console.log(`正在初始化图表 ${chart.id}...`);
                    Plotly.newPlot(chart.id, chart.data.data, chart.data.layout)
                        .then(() => console.log(`图表 ${chart.id} 初始化成功`))
                        .catch(error => console.error(`图表 ${chart.id} 初始化失败:`, error));
                } else {
                    console.warn(`图表 ${chart.id} 数据不完整:`, chart.data);
                }
            });
        } catch (error) {
            console.error('图表初始化过程中发生错误:', error);
        }
    } else {
        console.error('没有找到图表数据 (window.chartData 未定义)');
    }

    // 处理标题框点击事件
    const titleBoxes = document.querySelectorAll('.title-box');
    titleBoxes.forEach(box => {
        box.addEventListener('click', function() {
            // 移除所有标题框的active类
            titleBoxes.forEach(b => b.classList.remove('active'));
            // 添加当前标题框的active类
            this.classList.add('active');

            // 获取要显示的图表ID
            const chartId = this.getAttribute('data-chart');
            
            // 隐藏所有图表
            document.querySelectorAll('.chart').forEach(chart => {
                chart.classList.remove('active');
            });
            
            // 显示选中的图表
            document.getElementById(chartId).classList.add('active');
        });
    });
}); 