import React from 'react';
import DataSelector from './DataSelector';
import {getSeriesKeyBreakdown} from './CustomChartRepository';

function ScatterCreator(props) {
    const data = props.data;
    const chart = props.chart;
    const setChart = props.setChart;
    const dataFormat = getSeriesKeyBreakdown(data);

    const xAxisOptions = [{value: 'x', name: 'x'}];
    const yAxisOptions = [{value: 'y', name: 'y'}];
    const radiusOptions = [{value: 'radius', name: 'radius'}];

    const setXData = data => {
        setChart({
            ...chart,
            scatter: {
                ...chart.scatter,
                x: data
            }
        });
    };

    const setYData = data => {
        setChart({
            ...chart,
            scatter: {
                ...chart.scatter,
                y: data
            }
        });
    };

    const setRadiusData = data => {
        setChart({
            ...chart,
            scatter: {
                ...chart.scatter,
                radius: data
            }
        });
    };

    return (
        <div className='seriesCreator'>
            <DataSelector dataFormat={dataFormat} data={chart.scatter.x} setData={setXData} axisTypes={xAxisOptions} wildcard/>
            <DataSelector dataFormat={dataFormat} data={chart.scatter.y} setData={setYData} axisTypes={yAxisOptions} wildcard/>
            <DataSelector dataFormat={dataFormat} data={chart.scatter.radius} setData={setRadiusData} axisTypes={radiusOptions} wildcard/>
        </div>
    );
}

export default ScatterCreator;
