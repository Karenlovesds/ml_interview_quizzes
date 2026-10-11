const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const LETTERS = ["A", "B", "C", "D", "E", "F"];

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${path} -> ${res.status}`);
  return res.json();
}

/* ------------------------------------------------------------- tabs */
$$(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    $$(".tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    $$(".view").forEach((v) => v.classList.remove("active"));
    $(`#view-${tab.dataset.view}`).classList.add("active");
    if (tab.dataset.view === "weak") loadWeakness();
    if (tab.dataset.view === "kb") loadCorpus();
  });
});

/* ------------------------------------------------------------- quiz */
const state = {
  questions: [],
  index: 0,
  score: 0,
  answered: false,
  topic: "all",
  topicName: "All topics",
};

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

async function loadTopics() {
  const topics = await api("/api/topics");
  const sel = $("#topic-select");
  topics.forEach((t) => {
    const opt = document.createElement("option");
    opt.value = t.slug;
    opt.textContent = t.name;
    sel.appendChild(opt);
  });
  return topics;
}

async function startQuiz() {
  const topic = $("#topic-select").value;
  const mode = $("#mode-select").value;
  const order = $("#order-select").value;
  state.topic = topic;
  state.topicName = $("#topic-select").selectedOptions[0].textContent;

  const params = new URLSearchParams({ topic, mode });
  const data = await api(`/api/quiz?${params}`);
  let questions = data.questions;
  if (!questions.length) {
    $("#setup-hint").textContent =
      "No questions match that filter. Try a different topic or mode.";
    return;
  }
  if (order === "shuffle") questions = shuffle(questions);

  state.questions = questions;
  state.index = 0;
  state.score = 0;
  state.answered = false;

  $("#quiz-setup").classList.add("hidden");
  $("#quiz-done").classList.add("hidden");
  $("#quiz-run").classList.remove("hidden");
  renderQuestion();
}

function renderQuestion() {
  const q = state.questions[state.index];
  state.answered = false;

  $("#q-progress").textContent = `Question ${state.index + 1} / ${state.questions.length}`;
  $("#q-score").textContent = `Score ${state.score}`;
  $("#progress-fill").style.width = `${(state.index / state.questions.length) * 100}%`;
  $("#q-topic").textContent = state.topicName;
  $("#q-text").textContent = q.question;

  const box = $("#q-options");
  box.innerHTML = "";
  q.options.forEach((optText, i) => {
    const btn = document.createElement("button");
    btn.className = "option";
    btn.innerHTML = `<span class="key">${LETTERS[i]}</span><span>${escapeHtml(optText)}</span>`;
    btn.addEventListener("click", () => answer(i));
    box.appendChild(btn);
  });

  const fb = $("#q-feedback");
  fb.className = "feedback hidden";
  fb.innerHTML = "";
  $("#next-btn").classList.add("hidden");
  $("#finish-btn").classList.add("hidden");
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

async function answer(choice) {
  if (state.answered) return;
  state.answered = true;

  const q = state.questions[state.index];
  const data = await api("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question_id: q.id, choice }),
  });

  const buttons = $$("#q-options .option");
  buttons.forEach((btn, i) => {
    btn.disabled = true;
    if (i === data.answer) btn.classList.add("correct");
    if (i === choice && !data.correct) btn.classList.add("wrong");
  });

  if (data.correct) state.score += 1;
  $("#q-score").textContent = `Score ${state.score}`;

  const fb = $("#q-feedback");
  fb.className = `feedback ${data.correct ? "good" : "bad"}`;
  fb.innerHTML = `
    <div class="verdict">${data.correct ? "Correct" : "Incorrect"}</div>
    <div class="explain"><b>Answer:</b> ${escapeHtml(data.answer_text)}<br>${escapeHtml(data.explanation)}</div>
  `;

  const isLast = state.index === state.questions.length - 1;
  $("#next-btn").classList.toggle("hidden", isLast);
  $("#finish-btn").classList.toggle("hidden", !isLast);
}

function nextQuestion() {
  state.index += 1;
  renderQuestion();
}

function finishQuiz() {
  const total = state.questions.length;
  const pct = Math.round((state.score / total) * 100);
  $("#done-summary").textContent = `${state.score} / ${total} correct (${pct}%)`;
  $("#done-topic").textContent =
    pct >= 80
      ? "Strong performance — try another topic or the weakness report."
      : "Review the explanations and check your weakness report below.";
  $("#quiz-run").classList.add("hidden");
  $("#quiz-done").classList.remove("hidden");
  $("#progress-fill").style.width = "100%";
}

$("#start-btn").addEventListener("click", startQuiz);
$("#next-btn").addEventListener("click", nextQuestion);
$("#finish-btn").addEventListener("click", finishQuiz);
$("#again-btn").addEventListener("click", () => {
  $("#quiz-done").classList.add("hidden");
  $("#quiz-setup").classList.remove("hidden");
});
$("#quit-btn").addEventListener("click", () => {
  $("#quiz-run").classList.add("hidden");
  $("#quiz-setup").classList.remove("hidden");
});
$("#to-weak-btn").addEventListener("click", () => {
  document.querySelector('.tab[data-view="weak"]').click();
});

/* ------------------------------------------------------------- knowledge base */
let kbLoaded = false;

async function loadCorpus() {
  if (kbLoaded) return;
  kbLoaded = true;
  const items = await api("/api/corpus");
  const ul = $("#kb-topics");
  ul.innerHTML = "";
  items.forEach((item, idx) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.textContent = item.title;
    btn.addEventListener("click", () => openArticle(item.slug, btn));
    li.appendChild(btn);
    ul.appendChild(li);
  });
  if (items.length) ul.querySelector("button").click();
}

async function openArticle(slug, btn) {
  $$("#kb-topics button").forEach((b) => b.classList.remove("active"));
  if (btn) btn.classList.add("active");
  const data = await api(`/api/corpus/${slug}`);
  $("#kb-body").innerHTML = data.html;
}

/* ------------------------------------------------------------- weakness */
async function loadWeakness() {
  const r = await api("/api/weakness");

  const acc = r.overall_accuracy === null ? "—" : `${Math.round(r.overall_accuracy * 100)}%`;
  $("#weak-overview").innerHTML = `
    <div class="stat-card"><div class="value">${r.total_attempts}</div><div class="label">Questions answered</div></div>
    <div class="stat-card"><div class="value">${r.total_correct}</div><div class="label">Correct</div></div>
    <div class="stat-card"><div class="value">${acc}</div><div class="label">Overall accuracy</div></div>
    <div class="stat-card"><div class="value">${r.weak_topics.length}</div><div class="label">Weak topics (&lt;80%)</div></div>
  `;

  const topicsBox = $("#weak-topics");
  if (!r.topics.length) {
    topicsBox.innerHTML = `<p class="hint">No attempts yet — take a quiz first.</p>`;
  } else {
    topicsBox.innerHTML = r.topics
      .map((t) => {
        const pct = t.accuracy === null ? 0 : Math.round(t.accuracy * 100);
        const color = pct >= 80 ? "var(--good)" : pct >= 50 ? "var(--warn)" : "var(--bad)";
        return `<div class="topic-row">
          <span class="tname">${escapeHtml(t.name)}</span>
          <span class="bar"><span style="width:${pct}%;background:${color}"></span></span>
          <span class="tacc">${pct}%<br><small>${t.correct}/${t.attempts}</small></span>
        </div>`;
      })
      .join("");
  }

  const qBox = $("#weak-questions");
  if (!r.wrong_questions.length) {
    qBox.innerHTML = `<p class="hint">No wrong answers recorded yet. Nice.</p>`;
  } else {
    qBox.innerHTML = r.wrong_questions
      .map((q) => {
        const answerRow = q.options[q.answer];
        return `<div class="weak-item">
          <div class="wq">${escapeHtml(q.question)}</div>
          <div class="meta">${escapeHtml(q.topic_name)} · missed ${q.wrong_count}×
            <span class="badge">weak</span></div>
          <div class="ans"><b>Correct answer:</b> ${escapeHtml(answerRow)}</div>
          <div class="exp">${escapeHtml(q.explanation)}</div>
        </div>`;
      })
      .join("");
  }
}

$("#reset-btn").addEventListener("click", async () => {
  if (!confirm("Clear all quiz history? This cannot be undone.")) return;
  await api("/api/reset", { method: "POST" });
  loadWeakness();
});

/* ------------------------------------------------------------- init */
loadTopics();
