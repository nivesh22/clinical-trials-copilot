"use client"
import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

export function Sparkline({ data, width = 320, height = 80 }: { data: number[]; width?: number; height?: number }) {
  const ref = useRef<SVGSVGElement | null>(null)
  useEffect(() => {
    if (!ref.current || !data.length) return
    const svg = d3.select(ref.current)
    svg.selectAll('*').remove()
    const x = d3.scaleLinear().domain([0, data.length - 1]).range([0, width])
    const y = d3.scaleLinear().domain([0, d3.max(data) || 1]).range([height - 2, 2])
    const line = d3
      .line<number>()
      .x((_, i) => x(i))
      .y((d) => y(d))
      .curve(d3.curveMonotoneX)
    svg
      .append('path')
      .attr('d', line(data) || '')
      .attr('fill', 'none')
      .attr('stroke', '#2563eb')
      .attr('stroke-width', 2)
  }, [data, width, height])
  return <svg ref={ref} width={width} height={height} role="img" aria-label="Ingest sparkline" />
}

