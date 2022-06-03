/*
 * SolLewittSvg
 *
 * For course: https://www.freecodecamp.org/news/data-visualizatoin-with-d3/
 *
 * Uses JS Class template:
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
**/


SVG_NS_URL = 'http://www.w3.org/2000/svg'


class SolLewittD3 {
  constructor() {
  }

  /*
   * Static Methods
  **/
  static dev(parentId) {
    const canvasWidth = 400
    const canvasHeight = 400
    const parent = d3.select(`#${parentId}`)

    // Create SVG
    const svg = parent
      .append('svg')
      .attr('width', canvasWidth)
      .attr('height', canvasHeight)

    // Create SVG background: rows
    const rowHeight = 10
    const numRows = canvasHeight / rowHeight
    svg.selectAll('rect')
      .data(d3.range(numRows))
      .join('rect')
      .attr('y', (n) => n * 10)
      .attr('width', canvasWidth)
      .attr('height', rowHeight)
      .attr('fill', (n) => n % 2 == 0 ? 'black' : 'white')

    // Create SVG foreground: columns in circle
    const circleRadius = canvasHeight / 3
    const colWidth = 10
    const numCols = canvasWidth / colWidth
    const posLeft = 0
    const posTop = (canvasHeight / 2) - circleRadius
    const styleAttr = `position: absolute; left: ${posLeft}px; top: ${posTop}px`
    const fgSvg = parent
      .append('svg')
      .attr('width', canvasWidth)
      .attr('height', canvasHeight)
      .attr('style', styleAttr)

    fgSvg.selectAll('rect')
      .data(d3.range(numCols))
      .join('rect')
      .attr('x', (n) => n * 10)
      .attr('y', 0)
      .attr('width', colWidth)
      .attr('height', canvasHeight)
      .attr('fill', (n) => n % 2 == 0 ? 'black' : 'white')

    // Create column mask: cut out columns in circle
    const colMaskId = 'col-mask'
    const colMask = fgSvg.append('mask').attr('id', colMaskId)
    const colMaskRect = colMask.append('rect')
      .attr('width', canvasWidth)
      .attr('height', canvasHeight)
      .attr('fill', 'black')
    const colMaskCircle = colMask.append('circle')
      .attr('r', circleRadius)
      .attr('cx', canvasWidth / 2)
      .attr('cy', canvasHeight / 2)
      .attr('fill', 'white')

    // Apply mask
    fgSvg.attr('mask', `url(#${colMaskId})`)
  }

  static reproduce(parentId) {
    const canvasWidth = 400
    const canvasHeight = 400
    const parent = document.getElementById(parentId)

    // Create SVG and append to parent element
    const sol = new SolLewittD3()

    // Create background SVG: rows
    const bgSvg = sol.createSvgEl('svg', {width: canvasWidth, height: canvasHeight})

    const rowHeight = 10
    const numRows = canvasHeight / rowHeight
    for (let i = 0; i < numRows; i++) {
      let fillColor = i % 2 == 0 ? 'black' : 'white'
      let y = i * 10
      let row = sol.createRect(canvasWidth, rowHeight, 0, y, {fill: fillColor})
      bgSvg.appendChild(row)
    }

    parent.appendChild(bgSvg)

    // Create foreground SVG: columns in circle
    const circleRadius = canvasHeight / 3
    const fgSvg = sol.createSvgEl('svg', {
      width: canvasWidth,
      height: canvasHeight
    })
    fgSvg.style.position = 'absolute'
    fgSvg.style.top = `${(canvasHeight / 2) - circleRadius}px`
    fgSvg.style.left = '0px'

    const colWidth = 10
    const numCols = canvasWidth / colWidth
    for (let i = 0; i < numCols; i++) {
      let fillColor = i % 2 == 0 ? 'black' : 'white'
      let x = i * 10
      let col = sol.createRect(colWidth, canvasHeight, x, 0, {fill: fillColor})
      fgSvg.appendChild(col)
    }

    parent.appendChild(fgSvg)

    // Create column mask: cut out columns in circle
    const colMask = sol.createSvgEl('mask')
    colMask.setAttribute('id', 'col-mask')
    fgSvg.appendChild(colMask)

    const colMaskRect = sol.createSvgEl('rect')
    colMaskRect.setAttribute('width', canvasWidth)
    colMaskRect.setAttribute('height', canvasHeight)
    colMaskRect.setAttribute('fill', 'black')
    colMask.append(colMaskRect)

    const colMaskCircle = sol.createCircle(
      circleRadius,
      canvasWidth / 2,
      canvasHeight / 2,
      {fill: 'white'}
    )
    colMask.append(colMaskCircle)

    fgSvg.setAttribute('mask', 'url(#col-mask)')
  }

  /*
   * Getters
  **/

  /*
   * Methods
  **/
  createSvgEl(el, attrs) {
    attrs = attrs !== undefined ? attrs : {}
    const svg = document.createElementNS(SVG_NS_URL, el)
    for (const [attr, value] of Object.entries(attrs)) {
      svg.setAttribute(attr, value)
    }
    return svg
  }

  createRect(width, height, x, y, attrs) {
    const rectAttrs = {
      width: width,
      height: height,
      x: x,
      y: y
    }
    const elAttrs = Object.assign(rectAttrs, attrs)
    return this.createSvgEl('rect', elAttrs)
  }

  createCircle(r, cx, cy, attrs) {
    const rectAttrs = {
      r: r,
      cx: cx,
      cy: cy
    }
    const elAttrs = Object.assign(rectAttrs, attrs)
    return this.createSvgEl('circle', elAttrs)
  }

  createMask(el, id) {
    const attrs = {
      id: id,
      'data-url': `url(#${id})`
    }
    return this.createSvgEl('mask', attrs)
  }
}
