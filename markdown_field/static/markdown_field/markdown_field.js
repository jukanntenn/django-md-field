(function () {
  function debounce(fn, waitMs) {
    let timeoutId = null
    return (...args) => {
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => fn(...args), waitMs)
    }
  }

  function setTab(container, tabName) {
    const writeBtn = container.querySelector('[data-md-tab="write"]')
    const previewBtn = container.querySelector('[data-md-tab="preview"]')
    const writePane = container.querySelector('[data-md-pane="write"]')
    const previewPane = container.querySelector('[data-md-pane="preview"]')

    const isPreview = tabName === "preview"
    if (writeBtn) writeBtn.setAttribute("aria-selected", String(!isPreview))
    if (previewBtn) previewBtn.setAttribute("aria-selected", String(isPreview))
    if (writePane) writePane.hidden = isPreview
    if (previewPane) previewPane.hidden = !isPreview
  }

  function getCsrfTokenFromForm(container) {
    const form = container.closest("form")
    if (!form) return null
    const input = form.querySelector('input[name="csrfmiddlewaretoken"]')
    return input?.value || null
  }

  function initMarkdownField(container) {
    const textarea = container.querySelector("textarea")
    const previewEl = container.querySelector("[data-md-preview]")
    const previewUrl = container.dataset.mdPreviewUrl || ""
    const debounceMs = parseInt(container.dataset.mdDebounceMs, 10) || 300
    const fieldCacheKey = container.dataset.mdFieldCacheKey || ""

    if (!textarea || !previewEl) return

    let abortController = null
    let lastRenderedText = null

    async function renderPreview() {
      if (!previewUrl) {
        previewEl.textContent = gettext("Preview endpoint not configured")
        return
      }

      const text = textarea.value || ""
      if (text === lastRenderedText && previewEl.innerHTML) return

      const csrfToken = getCsrfTokenFromForm(container)
      if (!csrfToken) {
        previewEl.textContent = gettext(
          "Missing CSRF token (ensure form includes csrfmiddlewaretoken)"
        )
        return
      }

      if (abortController) abortController.abort()
      abortController = new AbortController()

      const body = new URLSearchParams()
      body.set("text", text)
      body.set("csrfmiddlewaretoken", csrfToken)
      body.set("field_cache_key", fieldCacheKey)

      try {
        const res = await window.fetch(previewUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: body.toString(),
          signal: abortController.signal,
        })

        if (!res.ok) {
          previewEl.textContent = interpolate(
            gettext("Preview request failed (%(status)s)"),
            { status: res.status },
            true
          )
          return
        }

        const data = await res.json()
        if (!data || typeof data.html !== "string") {
          previewEl.textContent = gettext("Invalid preview response format")
          return
        }

        previewEl.innerHTML = data.html
        lastRenderedText = text
      } catch (err) {
        if (err && err.name === "AbortError") return
        previewEl.textContent = gettext("Preview request error")
      }
    }

    const renderPreviewDebounced = debounce(renderPreview, debounceMs)

    const writeBtn = container.querySelector('[data-md-tab="write"]')
    const previewBtn = container.querySelector('[data-md-tab="preview"]')

    if (writeBtn) {
      writeBtn.addEventListener("click", () => {
        setTab(container, "write")
      })
    }

    if (previewBtn) {
      previewBtn.addEventListener("click", () => {
        setTab(container, "preview")
        renderPreviewDebounced()
      })
    }
  }

  function initAll() {
    document.querySelectorAll("[data-md-field]").forEach(initMarkdownField)
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll)
  } else {
    initAll()
  }
})()
