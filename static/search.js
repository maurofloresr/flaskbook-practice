// search.js — AJAX live search for unenrolled sports

const input = document.querySelector("#search")

// only run on pages that have the search input
if (input) {
  input.addEventListener("input", async function () {

    const response = await fetch("/search?q=" + input.value)
    const data = await response.json()

    const tbody = document.querySelector("#sport-list")
    tbody.innerHTML = ""

    data.forEach((sport, index) => {
      tbody.innerHTML += `
        <tr class="data-row">
          <td class="col-num muted">${index + 1}</td>
          <td class="sport-cell">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" class="sport-icon">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
            ${sport.sport}
          </td>
          <td class="col-action">
            <form action="/add" method="post">
              <input type="hidden" name="sport_id" value="${sport.id}">
              <button class="btn-add" type="submit">+ add</button>
            </form>
          </td>
        </tr>
      `
    })

    // if no results, show a message
    if (data.length === 0 && input.value.length > 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="3" style="padding:24px 16px;text-align:center;color:#888;font-size:13px;">
            No sports found for "${input.value}"
          </td>
        </tr>
      `
    }
  })
}