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
