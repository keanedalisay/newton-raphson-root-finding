import { updateMathJax } from './mathjax.js'

const newtonRaphsonForm = document.querySelector(
  'form[data-js="newton-raphson"]'
)
const resultsSection = document.querySelector('section[data-js="results-section"]')

newtonRaphsonForm.addEventListener('submit', async (event) => {
  event.preventDefault()

  const formData = new FormData(newtonRaphsonForm)
  const data = {
    function: formData.get('function'),
    initial_guess: parseFloat(formData.get('initial_guess')),
    tolerance: parseFloat(formData.get('tolerance'))
  }

  try {
    const response = await fetch(newtonRaphsonForm.action, {
      method: newtonRaphsonForm.method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    resultsSection.innerHTML = '' // Clear previous results

    resultsSection.insertAdjacentHTML(
      'beforeend',
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
  } catch (error) {
    console.error('Error: ', error)
  }
})
