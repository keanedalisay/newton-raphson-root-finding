import { updateMathJax } from './mathjax.js'

const functionInput = document.querySelector('input[data-js="function"]')
const functionText = document.querySelector('[data-js="function_preview"] span[data-js="function_text"]')

functionText.insertAdjacentHTML('beforeend', `\\(${functionInput.value}\\)`)

functionInput.addEventListener('input', function () {
  functionText.innerHTML = ''
  //
  //  Update the preview HTML and typeset the math
  //
  functionText.insertAdjacentHTML(
    'beforeend',
      `\\(f(x)\\) = \\(${functionInput.value}\\)`
  )

  updateMathJax()
})

function linspace (start, end, num) {
  const arr = []
  const step = (end - start) / (num - 1)
  for (let i = 0; i < num; i++) {
    arr.push(start + step * i)
  }
  return arr
}

document.addEventListener('DOMContentLoaded', () => {
  const plotDiv = document.getElementById('plot')
  const form = document.querySelector('[data-js="newton-raphson"]')

  if (!plotDiv || !form) return

  form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const fx = document.getElementById('function').value
    const x0 = parseFloat(document.getElementById('initial_guess').value)
    const tol = parseFloat(document.getElementById('tolerance').value)

    const res = await fetch('/api/newton-raphson/root', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ function: fx, initial_guess: x0, tolerance: tol })
    })

    const data = await res.json()
    if (!data.converged) {
      window.alert(data.message)
      return
    }

    const iterations = Object.values(data.iteration_table)
    const xs = iterations.map(r => r.x)
    const ys = iterations.map(r => r['f(x)'])

    const plotElementNow = document.getElementById('plot')
    if (!plotElementNow) return

    // Function curve
    const xCurve = linspace(Math.min(...xs) - 2, Math.max(...xs) + 2, 400)
    const yCurve = xCurve.map(x => math.evaluate(fx, { x }))

    const traceFunction = {
      x: xCurve,
      y: yCurve,
      type: 'scatter',
      mode: 'lines',
      name: 'f(x)',
      line: { color: 'royalblue', width: 3 }
    }

    const traceIterations = {
      x: [],
      y: [],
      mode: 'markers+lines',
      name: 'Newton iterations',
      hovertext: [],
      hoverinfo: 'text+name',
      line: { color: 'crimson', dash: 'dot', width: 2 },
      marker: { color: 'crimson', size: 8 }
    }

    const traceTangent = {
      x: [],
      y: [],
      mode: 'lines',
      name: 'Tangent',
      line: { color: 'orange', dash: 'dash', width: 2 }
    }

    const layout = {
      title: { text: 'Newton-Raphson Method', font: { size: 22 } },
      xaxis: { title: 'x', zeroline: true, showgrid: true, gridcolor: '#ddd' },
      yaxis: { title: 'f(x)', zeroline: true, showgrid: true, gridcolor: '#ddd' },
      plot_bgcolor: '#f9f9f9',
      paper_bgcolor: '#fff',
      legend: { x: 0.02, y: 0.98 },
      margin: { t: 50, b: 50, l: 50, r: 50 }
    }

    // Initial plot
    Plotly.newPlot(plotElementNow, [traceFunction, traceIterations, traceTangent], layout)

    // Animate iterations
    for (let i = 0; i < iterations.length; i++) {
      const r = iterations[i]
      const x_i = r.x
      const f_xi = r['f(x)']
      const deriv_xi = r["f'(x)"]

      // Update iteration points
      traceIterations.x.push(x_i)
      traceIterations.y.push(f_xi)
      traceIterations.hovertext.push(`Iter ${i}: x=${x_i.toFixed(4)}, f(x)=${f_xi.toFixed(4)}`)

      // Tangent line: y = f'(x_i)*(x - x_i) + f(x_i)
      const tangentX = [x_i - 1, x_i + 1]
      const tangentY = tangentX.map(xVal => deriv_xi * (xVal - x_i) + f_xi)

      traceTangent.x = tangentX
      traceTangent.y = tangentY

      Plotly.react(plotElementNow, [traceFunction, traceIterations, traceTangent], layout)

      // Wait for animation
      await new Promise(resolve => setTimeout(resolve, 4000))
    }

    // Remove tangent line at the end
    traceTangent.x = []
    traceTangent.y = []
    Plotly.react(plotElementNow, [traceFunction, traceIterations, traceTangent], layout)
  })
})
