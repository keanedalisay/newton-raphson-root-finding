import { updateMathJax } from './mathjax.js'

const newtonRaphsonForm = document.querySelector(
  'form[data-js="newton-raphson"]'
)
const functionInput = document.querySelector('input[data-js="function"]')
const functionPreview = document.querySelector('p[data-js="function_preview"]')
const resultsDiv = document.querySelector('div[data-js="results"]')

functionPreview.insertAdjacentHTML('beforeend', `\\(${functionInput.value}\\)`)

functionInput.addEventListener('input', function () {
  functionPreview.innerHTML = ''
  //
  //  Update the preview HTML and typeset the math
  //
  functionPreview.insertAdjacentHTML(
    'beforeend',
      `\\(${functionInput.value}\\)`
  )

  updateMathJax()
})

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

    resultsDiv.insertAdjacentHTML(
      'beforeend',
      `
      <p>Root: ${result.root_approximation}</p>
      <p>Iterations: ${result.iterations}</p>
      <p>Converged: ${result.converged}</p>
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
          <td>${i}</td>
          <td>${row.x}</td>
          <td>${row['f(x)']}</td>
          <td>${row["f'(x)"]}</td>
        </tr>`
    }

    tableHTML += '</table><hr>'

    resultsDiv.insertAdjacentHTML('beforeend', tableHTML)

    updateMathJax()
  } catch (error) {
    console.error('Error: ', error)
  }
})
