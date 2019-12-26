import moment from 'moment';

const chartOptionsChart = {
	chart: {
		fontFamily: 'Press Start 2P',
		stacked: false,
		height: 300,
		toolbar: {
			show: false,
		},

	},
	dataLabels: {
		enabled: false
	},
	series: [{
		name: '',
		data: []
	}],
	markers: {
		size: 0,
	},
	title: {
		text: 'Time series',
		align: 'left',
		style: {
			fontSize: '10px',
		},

	},
	legend: {
		show: true,
	},
	fill: {
		type: 'solid'
	},
	yaxis: {
		labels: {
			formatter: function (val) {
				return (val / 1000) + "k";
			},
		},
		tickAmount: 1,
		min: 0,
		max: 1000,
		style: {
			fontSize: '10px',
		},
	},
	xaxis: {
		show: false,
		type: 'datetime',
		style: {
			fontSize: '10px',
		},
	},
	stroke: {
		curve: 'smooth'
	},
	tooltip: {
		shared: false,
		y: {
			formatter: function (val) {
				return (val)
			}
		}
	},
}

export {chartOptionsChart}
