
import React, { useEffect } from 'react'
import * as d3 from 'd3'
import {Types} from '../types/data'

const BasicScatterChart = (props: IBasicScatterChartProps) => {
  useEffect(() => {
    draw()
  })
  const draw = () => {
    const width = props.width - props.left - props.right
    const height = props.height - props.top - props.bottom

    const svg = d3
      .select('.basicScatterChart')
      .append('svg')
      .attr('width', width + props.left + props.right)
      .attr('height', height + props.top + props.bottom)
      .append('g')
      .attr('transform', `translate(${props.left},${props.top})`)

    d3.dsv(',', '/data/scatter.csv', (d) => {
      return {
        price: d.price,
        carat: d.carat,
      }
    }).then((data) => {
        const maxPrice = 8000
        const maxCarat = 0.8
        const x = d3.scaleLinear().domain([0, 18000]).range([0, width])
        svg.append('g').attr('transform', `translate(0,${height})`).call(d3.axisBottom(x))

        const y = d3.scaleLinear().domain([0, 4.5]).range([height, 0])
        svg.append('g').call(d3.axisLeft(y))

        svg
        .append('g')
        .selectAll('dot')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', (d) => {
          return x(((d as unknown) as Types.Data).price)
        })
        .attr('cy', (d) => {
          return y(((d as unknown) as Types.Data).carat)
        })
        .attr('r', 0.8)
        .style('fill', props.fill)
    })
  }

  return <div className="basicScatterChart" />
}

interface IBasicScatterChartProps {
  width: number
  height: number
  top: number
  right: number
  bottom: number
  left: number
  fill: string
}

export default BasicScatterChart