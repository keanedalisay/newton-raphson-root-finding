let updatePending = false // true if an update is needed after MathJax completes

window.MathJax = {
  loader: { load: ['[tex]/begingroup'] },
  tex: {
    packages: { '[+]': ['begingroup'] },
    inlineMath: { '[+]': [['$', '$']] }
  },

  startup: {
    pageReady () {
      //
      //  Do the initial typesetting and update the preview if
      //  the textarea already contains content (e.g., on a page reload).
      //
      return window.MathJax.startup.defaultPageReady().then(() => {
        updateMathJax()
      })
    }
  }
}

export function updateMathJax () {
  if (window.MathJax) {
    updatePending = false

    //
    //  Reset any TeX labels or equation numbers
    //  Start a new sandbox for new macro definitions (and remove any old ones)
    //
    window.MathJax.texReset()
    window.MathJax.tex2mml('\\begingroupSandbox')

    window.MathJax.typesetPromise()
      .then(() => {
        //
        //  MathJax has completed, so is no longer running
        //  If an update was needed while MathJax was running, update the
        //    preview again.
        //

        if (updatePending) updateMathJax()
      })
      .catch((err) => console.error('Math typeset failed:', err))
  }
}
