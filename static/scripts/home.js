import { updateMathJax } from './mathjax.js'

const newtonRaphsonForm = document.querySelector(
  'form[data-js="newton-raphson"]'
)
const resultsSection = document.querySelector('section[data-js="results-section"]')
const resultsPlot = resultsSection.querySelector('#plot')

newtonRaphsonForm.addEventListener('submit', async (event) => {
  event.preventDefault()
  displayNewtonRaphsonResults()
  displayNewtonRaphsonPlot()
})

async function displayNewtonRaphsonResults () {
  const formData = new FormData(newtonRaphsonForm)
  const data = {
    function: formData.get('function'),
    initial_guess: parseFloat(formData.get('initial_guess')),
    tolerance: parseFloat(formData.get('tolerance'))
  }

  const response = await fetch(newtonRaphsonForm.action, {
    method: newtonRaphsonForm.method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  const result = await response.json()

  resultsSection.innerHTML = ''
  resultsPlot.innerHTML = ''
  if (resultsPlot) resultsSection.appendChild(resultsPlot)

  if (result.status !== 200) {
    resultsSection.insertAdjacentHTML(
      'afterbegin',
      `
      <h2 class="error">Status Code: ${result.status}</h2>
      <p class="error">${result.message}</p>
      <hr>
      `
    )

    updateMathJax()

    return
  }

  resultsSection.insertAdjacentHTML(
    'afterbegin',
    `
    <h2>Root-Finding Results</h2>
    <p>With <b>${result.iterations} iterations</b>, the approximate root is <b>${result.root_approximation}</b>.</p>
    <p>The function value at this root approximation is <b>${result.function_value_at_root}</b>.</p>
    <p>The derivative value at this root approximation is <b>${result.derivative_value_at_root}</b>.</p>
    <hr>
    `
  )

  let tableHTML = `
    <table border="1">
      <tr>
        <th>Iteration</th>
        <th>\\(x_n\\)</th>
        <th>\\(f(x_n)\\)</th>
        <th>\\(f'(x_n)\\)</th>
      </tr>
  `
  for (const [i, row] of Object.entries(result.iteration_table)) {
    tableHTML += `
      <tr>
        <td>${parseInt(i)}</td>
        <td>${row.x}</td>
        <td>${row['f(x)']}</td>
        <td>${row["f'(x)"]}</td>
      </tr>`
  }

  tableHTML += '</table><hr>'

  resultsSection.insertAdjacentHTML('beforeend', tableHTML)

  updateMathJax()
}

async function displayNewtonRaphsonPlot () {
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
    resultsPlot.insertAdjacentHTML(
      'beforeend',
      `
      <p class="error">No available plot for the function</p>
      <hr>
      `
    )

    updateMathJax()
    return
  }

  const iterations = Object.values(data.iteration_table)
  const xs = iterations.map(r => r.x)
  const ys = iterations.map(r => r['f(x)'])

  resultsPlot.style.height = '500px'
  resultsPlot.innerHTML = ''
  if (!resultsPlot) return

  try {
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
      name: 'iteration',
      hovertext: [],
      hoverinfo: 'text+name',
      line: { color: 'crimson', dash: 'dot', width: 2 },
      marker: { color: 'crimson', size: 8 }
    }

    const traceTangent = {
      x: [],
      y: [],
      mode: 'lines',
      name: 'tangent line',
      line: { color: 'orange', dash: 'dash', width: 2 }
    }

    const layout = {
      title: { text: `Plotting f(x) = ${fx}`, font: { size: 16 } },
      xaxis: { title: 'x', zeroline: true, showgrid: true, gridcolor: '#ddd' },
      yaxis: { title: 'f(x)', zeroline: true, showgrid: true, gridcolor: '#ddd' },
      plot_bgcolor: '#f0f0f0',
      paper_bgcolor: '#f5f5f5',
      legend: { x: 0.02, y: 0.98 },
      margin: { t: 50, b: 50, l: 50, r: 50 }
    }

    // Initial plot
    Plotly.newPlot(resultsPlot, [traceFunction, traceIterations, traceTangent], layout)

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

      Plotly.react(resultsPlot, [traceFunction, traceIterations, traceTangent], layout)

      // Wait for animation
      await new Promise(resolve => setTimeout(resolve, 4000))
    }

    // Remove tangent line at the end
    traceTangent.x = []
    traceTangent.y = []
    Plotly.react(resultsPlot, [traceFunction, traceIterations, traceTangent], layout)
  } catch (err) {
    resultsPlot.style.height = 'auto'
    resultsPlot.insertAdjacentHTML(
      'beforeend',
      `
      <p class="error">No available plot for the function</p>
      <hr>
      `
    )

    updateMathJax()
  }
}

function linspace (start, end, num) {
  const arr = []
  const step = (end - start) / (num - 1)
  for (let i = 0; i < num; i++) {
    arr.push(start + step * i)
  }
  return arr
}
