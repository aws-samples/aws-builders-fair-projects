const colors = {
	black: '#000000',
	blue: '#2255FF',
	lightBlue: '#448aFF',
	orange: '#FFAA00',
	red: '#FF5533',
}

const dataLabels = {
	enabled: true,
	enabledOnSeries: undefined,

	style: {
		fontSize: '10px',
		colors: [colors.black],
	},
}

const title = {
	text: 'Water Level',
	align: 'left',
	style: {
		fontSize: '10px',
	},
	margin: -20,
}

const moistureRange = {
	min: 0,
	empty: 200,
	almostEmpty: 300,
	middle: 500,
	max: 3000,
}

const ranges = [{
	from: moistureRange.min,
	to: moistureRange.empty,
	color: colors.red,
	name: 'empty',
}, {
	from: moistureRange.empty,
	to: moistureRange.almostEmpty,
	color: colors.orange,
	name: 'almost empty',
}, {
	from: moistureRange.almostEmpty,
	to: moistureRange.middle,
	color: colors.lightBlue,
	name: '',
}, {
	from: moistureRange.middle,
	to: moistureRange.max,
	color: colors.blue,
	name: '',
}]

const plotOptions = {
	heatmap: {
		enableShades: false,
		colorScale: {
			ranges: ranges
		},
	}
}

const legend = {
	show: false,
}

const chart = {
	toolbar: {
		show: false,
	},
	fontFamily: 'Press Start 2P',

}

const chartOptionsHeatMap = {
	plotOptions: plotOptions,
	dataLabels: dataLabels,
	title: title,
	legend: legend,
	chart: chart,
	tooltip: {
		enabled: false,
	},
}

export {chartOptionsHeatMap}
