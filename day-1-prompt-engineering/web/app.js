/**
 * COMSATS University Islamabad, Wah Campus
 * PromptCraft — Day 1 Prompt Engineering Studio
 * Client-Side Application Logic: Dynamic Flow Diagrams, Runtime Charts & Technique Audits
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const techniqueCards = document.getElementById('techniqueCards');
    const userPromptInput = document.getElementById('userPromptInput');
    const executePromptBtn = document.getElementById('executePromptBtn');
    const sampleChips = document.getElementById('sampleChips');

    // Architecture Diagram & Pipeline Elements
    const diagramHeaderTitle = document.getElementById('diagramHeaderTitle');
    const diagramHeaderSubtitle = document.getElementById('diagramHeaderSubtitle');
    const diagramViewToggle = document.getElementById('diagramViewToggle');
    const diagramViewTrack = document.getElementById('diagramViewTrack');
    const pipelineViewTrack = document.getElementById('pipelineViewTrack');
    const pipelineStatusTag = document.getElementById('pipelineStatusTag');
    const flowDiagramContainer = pipelineViewTrack || document.getElementById('flowDiagramContainer');
    const topicDiagramImg = document.getElementById('topicDiagramImg');
    const topicDiagramPills = document.getElementById('topicDiagramPills');

    // Model Response Elements
    const welcomePlaceholder = document.getElementById('welcomePlaceholder');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const loadingStageTitle = document.getElementById('loadingStageTitle');
    const loadingStageDetail = document.getElementById('loadingStageDetail');
    const responseContent = document.getElementById('responseContent');
    const responseText = document.getElementById('responseText');
    const responseCaption = document.getElementById('responseCaption');
    const latencyBadge = document.getElementById('latencyBadge');
    const copyBtn = document.getElementById('copyBtn');

    // Visualizations Elements
    const visPlaceholder = document.getElementById('visPlaceholder');
    const visRenderArea = document.getElementById('visRenderArea');
    const visDescription = document.getElementById('visDescription');
    const visTypeToggle = document.getElementById('visTypeToggle');

    // Engineered Prompt Inspection Elements
    const promptPlaceholder = document.getElementById('promptPlaceholder');
    const promptDetailsArea = document.getElementById('promptDetailsArea');
    const systemInstSection = document.getElementById('systemInstSection');
    const systemInstText = document.getElementById('systemInstText');
    const engineeredPromptText = document.getElementById('engineeredPromptText');
    const multiplierBadge = document.getElementById('multiplierBadge');

    // Technique Auditing Elements
    const techniquesPlaceholder = document.getElementById('techniquesPlaceholder');
    const techniquesList = document.getElementById('techniquesList');
    const techniqueStatusBadge = document.getElementById('techniqueStatusBadge');

    // Audit Log & Export
    const sessionLog = document.getElementById('sessionLog');
    const exportNotesBtn = document.getElementById('exportNotesBtn');

    // Runtime state (Technique 7 Iterative Prompt Ladder active by default)
    let selectedTechnique = "7";
    let currentRuntimeData = null;
    let activeChartType = "expansion";

    // Technique to Topic Diagram Map
    const TECHNIQUE_DIAGRAM_MAP = {
        "1": { svg: "diagrams/topic_03_zero_vs_few_shot.svg", title: "Topic 03: Zero-Shot vs Few-Shot Prompting", topic: "1" },
        "2": { svg: "diagrams/topic_03_zero_vs_few_shot.svg", title: "Topic 03: Zero-Shot vs Few-Shot Prompting", topic: "1" },
        "3": { svg: "diagrams/topic_04_decomposition.svg", title: "Topic 04: Task Decomposition Pipeline", topic: "3" },
        "4": { svg: "diagrams/topic_05_system_vs_user.svg", title: "Topic 05: System Instructions vs User Prompts", topic: "4" },
        "5": { svg: "diagrams/topic_06_structured_output.svg", title: "Topic 06: Structured Output & JSON Formatting", topic: "5" },
        "6": { svg: "diagrams/topic_02_anatomy.svg", title: "Topic 02: Anatomy of an Effective Prompt", topic: "6" },
        "7": { svg: "diagrams/topic_07_prompt_improvement.svg", title: "Topic 07: Iterative Prompt Improvement Ladder", topic: "7" }
    };

    // Topic Diagram Switching Helper
    function switchTopicDiagram(svgPath, title, topicId) {
        if (topicDiagramImg) {
            topicDiagramImg.style.opacity = '0.35';
            setTimeout(() => {
                topicDiagramImg.src = svgPath;
                topicDiagramImg.alt = title;
                topicDiagramImg.style.opacity = '1';
            }, 120);
        }
        if (diagramHeaderTitle) diagramHeaderTitle.textContent = title;
        if (topicDiagramPills) {
            topicDiagramPills.querySelectorAll('.topic-diagram-pill').forEach(pill => {
                if (pill.dataset.topic === String(topicId) || pill.dataset.svg === svgPath) {
                    pill.classList.add('active');
                } else {
                    pill.classList.remove('active');
                }
            });
        }
    }

    // Topic Diagram Pills Bar Click Handler
    if (topicDiagramPills) {
        topicDiagramPills.addEventListener('click', (e) => {
            const pill = e.target.closest('.topic-diagram-pill');
            if (pill) {
                const svg = pill.dataset.svg;
                const title = pill.dataset.title;
                const topic = pill.dataset.topic;
                switchTopicDiagram(svg, title, topic);

                // If user clicks a topic that matches a technique card, also sync the card
                if (techniqueCards && topic && topic !== 'flow' && topic !== '8') {
                    const card = techniqueCards.querySelector(`[data-type="${topic}"]`);
                    if (card) {
                        techniqueCards.querySelectorAll('.technique-card').forEach(c => c.classList.remove('active'));
                        card.classList.add('active');
                        selectedTechnique = topic;
                    }
                }
            }
        });
    }

    // Diagram View Toggle (Topic Diagram vs Execution Pipeline Trace)
    if (diagramViewToggle) {
        diagramViewToggle.addEventListener('click', (e) => {
            const btn = e.target.closest('.tab-pill');
            if (btn) {
                diagramViewToggle.querySelectorAll('.tab-pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const view = btn.dataset.view;
                if (view === 'diagram') {
                    if (diagramViewTrack) diagramViewTrack.classList.remove('hidden');
                    if (pipelineViewTrack) pipelineViewTrack.classList.add('hidden');
                    if (topicDiagramPills) topicDiagramPills.style.display = 'flex';
                    const activePill = topicDiagramPills ? topicDiagramPills.querySelector('.topic-diagram-pill.active') : null;
                    if (diagramHeaderTitle && activePill) diagramHeaderTitle.textContent = activePill.dataset.title;
                } else {
                    if (diagramViewTrack) diagramViewTrack.classList.add('hidden');
                    if (pipelineViewTrack) pipelineViewTrack.classList.remove('hidden');
                    if (topicDiagramPills) topicDiagramPills.style.display = 'none';
                    if (diagramHeaderTitle) diagramHeaderTitle.textContent = 'Live Execution Pipeline Trace';
                }
            }
        });
    }

    // Technique Selector Handler
    if (techniqueCards) {
        techniqueCards.addEventListener('click', (e) => {
            const card = e.target.closest('.technique-card');
            if (card) {
                techniqueCards.querySelectorAll('.technique-card').forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                selectedTechnique = card.dataset.type;

                // Sync diagram to this technique
                const mapInfo = TECHNIQUE_DIAGRAM_MAP[selectedTechnique];
                if (mapInfo) {
                    switchTopicDiagram(mapInfo.svg, mapInfo.title, mapInfo.topic);
                }

                // If currently on pipeline view, switch back to diagram view to show relevant architecture
                if (diagramViewToggle) {
                    const diagBtn = diagramViewToggle.querySelector('[data-view="diagram"]');
                    if (diagBtn && !diagBtn.classList.contains('active')) {
                        diagBtn.click();
                    }
                }
            }
        });
    }

    // Quick Starter Chips Handler
    if (sampleChips) {
        sampleChips.addEventListener('click', (e) => {
            const chip = e.target.closest('.query-pill');
            if (chip) {
                userPromptInput.value = chip.dataset.prompt;
                executePromptTransformation();
            }
        });
    }

    // Execute Button Handler
    if (executePromptBtn) {
        executePromptBtn.addEventListener('click', (e) => {
            e.preventDefault();
            executePromptTransformation();
        });
    }

    // Allow Ctrl+Enter in Textarea
    if (userPromptInput) {
        userPromptInput.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                executePromptTransformation();
            }
        });
    }

    // Chart Type Toggle Handler
    if (visTypeToggle) {
        visTypeToggle.addEventListener('click', (e) => {
            const btn = e.target.closest('.tab-pill');
            if (btn && currentRuntimeData) {
                visTypeToggle.querySelectorAll('.tab-pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeChartType = btn.dataset.chart;
                renderRuntimeVisualizations(currentRuntimeData);
            }
        });
    }

    // Copy Response Handler
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const text = responseText.innerText;
            if (text) {
                navigator.clipboard.writeText(text).then(() => {
                    const orig = copyBtn.innerHTML;
                    copyBtn.innerHTML = `
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        <span style="color:#059669; font-weight:600;">Copied</span>
                    `;
                    setTimeout(() => copyBtn.innerHTML = orig, 1800);
                });
            }
        });
    }

    // Export Experiment Notes Handler
    if (exportNotesBtn) {
        exportNotesBtn.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/export-history');
                if (!res.ok) throw new Error('Notes file not accessible.');
                const text = await res.text();
                const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'promptcraft_experiment_notes.md';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch (err) {
                alert('Export Notice: ' + err.message);
            }
        });
    }

    // =========================================================================
    // Core Execution Function
    // =========================================================================
    async function executePromptTransformation() {
        const promptText = userPromptInput.value.trim();
        if (!promptText) {
            userPromptInput.focus();
            return;
        }

        if (executePromptBtn.disabled) return;
        executePromptBtn.disabled = true;

        // UI State Transitions
        welcomePlaceholder.classList.add('hidden');
        responseContent.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');
        latencyBadge.classList.add('hidden');

        visPlaceholder.classList.add('hidden');
        visRenderArea.classList.add('hidden');
        visTypeToggle.style.display = 'none';

        promptPlaceholder.classList.add('hidden');
        promptDetailsArea.classList.add('hidden');

        techniquesPlaceholder.classList.add('hidden');
        techniquesList.classList.add('hidden');
        techniqueStatusBadge.textContent = 'Auditing...';

        // Render Dynamic Initial Pipeline State
        renderInitialFlowState(promptText);

        try {
            const res = await fetch('/api/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: selectedTechnique, prompt: promptText })
            });

            if (!res.ok) {
                throw new Error(`Server returned HTTP ${res.status}`);
            }

            const data = await res.json();
            currentRuntimeData = data;

            // 1. Render Completed Flow Diagram
            renderCompletedFlowDiagram(data);

            // 2. Render Model Response
            renderModelResponse(data);

            // 3. Render Runtime Visualizations
            renderRuntimeVisualizations(data);

            // 4. Render Prompt Payload Inspection
            renderPromptInspection(data);

            // 5. Render Technique Audits
            renderTechniqueAudits(data.techniques);

            // 6. Append to Experiment Audit Log
            appendToExperimentLog(data.technique, promptText, data.response, data.latency_sec);

        } catch (err) {
            console.error('Execution Error:', err);
            handleExecutionError(err);
        } finally {
            executePromptBtn.disabled = false;
        }
    }

    // =========================================================================
    // 1. Dynamic Flow Diagram Renderer
    // =========================================================================
    function renderInitialFlowState(promptText) {
        if (pipelineStatusTag) {
            pipelineStatusTag.className = 'status-pill status-active';
            pipelineStatusTag.textContent = 'Transforming & Inferring...';
        }

        const estTokens = Math.max(1, Math.round(promptText.length / 4));

        flowDiagramContainer.innerHTML = `
            <div class="flow-track">
                <div class="flow-node state-active">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 1</span>
                        <span class="flow-node-badge">Ingested</span>
                    </div>
                    <div class="flow-node-title">Raw Prompt Ingestion</div>
                    <div class="flow-node-summary">~${estTokens} tokens • Ready</div>
                    <div class="flow-node-detail">${escapeHtml(promptText.slice(0, 30))}${promptText.length > 30 ? '...' : ''}</div>
                </div>

                <div class="flow-connector">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </div>

                <div class="flow-node state-active">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 2</span>
                        <span class="flow-node-badge">Injecting</span>
                    </div>
                    <div class="flow-node-title">Technique Transformation</div>
                    <div class="flow-node-summary">Applying prompt rules...</div>
                    <div class="flow-node-detail">Technique #${selectedTechnique}</div>
                </div>

                <div class="flow-connector">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </div>

                <div class="flow-node state-pending">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 3</span>
                        <span class="flow-node-badge">Budget</span>
                    </div>
                    <div class="flow-node-title">Context Budgeting</div>
                    <div class="flow-node-summary">Calculating expansion...</div>
                    <div class="flow-node-detail">Cap: 1M tokens</div>
                </div>

                <div class="flow-connector">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </div>

                <div class="flow-node state-pending">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 4</span>
                        <span class="flow-node-badge">Inference</span>
                    </div>
                    <div class="flow-node-title">Gemini Model Inference</div>
                    <div class="flow-node-summary">Google GenAI processing...</div>
                    <div class="flow-node-detail">Temp: 0.2</div>
                </div>

                <div class="flow-connector">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </div>

                <div class="flow-node state-pending">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 5</span>
                        <span class="flow-node-badge">Validation</span>
                    </div>
                    <div class="flow-node-title">Output Validation</div>
                    <div class="flow-node-summary">Formatting compliance</div>
                    <div class="flow-node-detail">Pending output</div>
                </div>
            </div>
        `;
    }

    function renderCompletedFlowDiagram(data) {
        if (pipelineStatusTag) {
            pipelineStatusTag.className = 'status-pill status-completed';
            pipelineStatusTag.textContent = `Completed in ${data.latency_sec.toFixed(2)}s • ${data.expansion_multiplier}x Expansion`;
        }

        const stages = data.stages || [];
        if (!stages.length) return;

        let html = '<div class="flow-track">';
        stages.forEach((stage, idx) => {
            const stateClass = stage.status_class === 'completed' ? 'state-completed' :
                               stage.status_class === 'failed' ? 'state-failed' : 'state-active';

            html += `
                <div class="flow-node ${stateClass}" title="${escapeHtml(stage.summary)}">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage ${stage.step}</span>
                        <span class="flow-node-badge">${escapeHtml(stage.badge)}</span>
                    </div>
                    <div class="flow-node-title">${escapeHtml(stage.title)}</div>
                    <div class="flow-node-summary">${escapeHtml(stage.summary)}</div>
                    <div class="flow-node-detail">${escapeHtml(stage.detail)}</div>
                </div>
            `;

            if (idx < stages.length - 1) {
                html += `
                    <div class="flow-connector">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </div>
                `;
            }
        });
        html += '</div>';

        flowDiagramContainer.innerHTML = html;
    }

    // =========================================================================
    // 2. Model Response Presentation
    // =========================================================================
    function renderModelResponse(data) {
        loadingIndicator.classList.add('hidden');
        responseContent.classList.remove('hidden');

        responseCaption.textContent = `Technique Applied: ${data.technique}`;
        latencyBadge.textContent = `Latency: ${data.latency_sec.toFixed(2)}s`;
        latencyBadge.classList.remove('hidden');

        if (data.is_json) {
            try {
                const parsed = JSON.parse(data.response);
                responseText.innerHTML = `<pre style="font-family:var(--font-mono); font-size:12.5px; background:var(--color-surface-subtle); padding:14px; border-radius:6px; border:1px solid var(--color-border-subtle);">${escapeHtml(JSON.stringify(parsed, null, 2))}</pre>`;
                return;
            } catch (e) {
                // fallback to regular formatting
            }
        }

        // Clean markdown formatting
        let formatted = data.response.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/^\s*[\-\*]\s+(.*)$/gm, '<li>$1</li>');
        if (formatted.includes('<li>')) {
            formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul style="margin: 8px 0 12px 18px; padding-left: 4px;">$1</ul>');
        }
        responseText.innerHTML = formatted;
    }

    // =========================================================================
    // 3. Intelligent Runtime Visualizations
    // =========================================================================
    function renderRuntimeVisualizations(data) {
        visPlaceholder.classList.add('hidden');
        visRenderArea.classList.remove('hidden');
        visTypeToggle.style.display = 'inline-flex';

        const vis = data.visualization || {};
        visDescription.textContent = vis.description || 'Token expansion and context window budget metrics.';

        if (activeChartType === 'expansion') {
            renderTokenExpansionBarChart(vis.metrics || [], data.expansion_multiplier || 1.0);
        } else {
            renderTokenBudgetDistribution(data.token_budget || {}, vis.token_distribution || []);
        }
    }

    function renderTokenExpansionBarChart(metrics, multiplier) {
        if (!metrics || metrics.length === 0) return;

        const maxTokens = Math.max(...metrics.map(m => m.tokens), 10);
        const barHeight = 26;
        const barGap = 12;
        const labelWidth = 175;
        const chartWidth = 580;
        const chartHeight = metrics.length * (barHeight + barGap) + 40;
        const maxBarWidth = chartWidth - labelWidth - 80;

        let svgContent = `
            <svg class="chart-svg" viewBox="0 0 ${chartWidth} ${chartHeight}" preserveAspectRatio="xMinYMin meet">
                <!-- Axes -->
                <line x1="${labelWidth}" y1="10" x2="${labelWidth}" y2="${chartHeight - 20}" class="chart-axis-line" />
                <line x1="${labelWidth}" y1="${chartHeight - 20}" x2="${chartWidth - 20}" y2="${chartHeight - 20}" class="chart-axis-line" />
        `;

        metrics.forEach((item, idx) => {
            const y = 14 + idx * (barHeight + barGap);
            const barW = Math.max(4, (item.tokens / maxTokens) * maxBarWidth);

            svgContent += `
                <g class="chart-row">
                    <text x="${labelWidth - 10}" y="${y + 17}" text-anchor="end" class="chart-label">
                        ${escapeHtml(item.label)}
                    </text>
                    <rect 
                        x="${labelWidth + 2}" 
                        y="${y}" 
                        width="${barW}" 
                        height="${barHeight}" 
                        fill="${item.color || '#0F172A'}" 
                        rx="4"
                    >
                        <title>${escapeHtml(item.label)}: ${item.tokens} tokens</title>
                    </rect>
                    <text x="${labelWidth + barW + 10}" y="${y + 17}" class="chart-value-label">
                        ${item.tokens} tok
                    </text>
                </g>
            `;
        });

        svgContent += `
                <text x="${labelWidth}" y="${chartHeight - 6}" text-anchor="middle" class="chart-label" style="font-size: 10px;">
                    0 Tokens
                </text>
                <text x="${chartWidth - 40}" y="${chartHeight - 6}" text-anchor="middle" class="chart-label" style="font-size: 10px;">
                    Peak: ${maxTokens} tok
                </text>
            </svg>
        `;

        visRenderArea.innerHTML = `
            <div class="svg-chart-container">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; font-size:12px; color:var(--color-text-muted);">
                    <span>Expansion Multiplier: <strong>${multiplier}x</strong> context enlargement</span>
                    <span style="font-family:var(--font-mono);">Tokens Computed at Runtime</span>
                </div>
                ${svgContent}
            </div>
        `;
    }

    function renderTokenBudgetDistribution(budget, distribution) {
        const total = budget.total_tokens || 1;

        let segmentsHtml = '';
        let legendHtml = '';

        const classMap = {
            'Input': 'token-seg-query',
            'Technique Framing': 'token-seg-context',
            'Model Response': 'token-seg-response'
        };

        const colorMap = {
            'Input': '#3B82F6',
            'Technique Framing': '#0D9488',
            'Model Response': '#0F172A'
        };

        distribution.forEach(item => {
            const segClass = classMap[item.label] || 'token-seg-system';
            const color = colorMap[item.label] || '#64748B';

            segmentsHtml += `
                <div class="token-segment ${segClass}" style="width: ${Math.max(item.pct, 3)}%;" title="${escapeHtml(item.label)}: ${item.tokens} tokens (${item.pct}%)">
                    ${item.pct >= 8 ? `${item.pct}%` : ''}
                </div>
            `;

            legendHtml += `
                <div class="token-legend-item">
                    <span class="token-legend-label">
                        <span class="token-dot" style="background-color: ${color};"></span>
                        <span>${escapeHtml(item.label)}</span>
                    </span>
                    <span class="token-legend-val">${item.tokens} tok <small style="font-weight:400; color:var(--color-text-muted);">(${item.pct}%)</small></span>
                </div>
            `;
        });

        visRenderArea.innerHTML = `
            <div class="token-dist-wrapper">
                <div class="token-bar-track">
                    ${segmentsHtml}
                </div>
                <div class="token-legend-grid">
                    ${legendHtml}
                </div>
                <div style="font-size: 11.5px; color: var(--color-text-muted); padding-top: 4px; border-top: 1px solid var(--color-border-subtle);">
                    Total Tokens Exchanged: <strong>${total} tokens</strong> • Context Framing Ratio: <strong>${Math.round((budget.engineered_tokens || 0) / total * 100)}%</strong>
                </div>
            </div>
        `;
    }

    // =========================================================================
    // 4. Engineered Prompt Payload Inspection
    // =========================================================================
    function renderPromptInspection(data) {
        promptPlaceholder.classList.add('hidden');
        promptDetailsArea.classList.remove('hidden');

        multiplierBadge.textContent = `${data.expansion_multiplier}x Expansion`;

        if (data.system_instruction) {
            systemInstText.textContent = data.system_instruction;
            systemInstSection.classList.remove('hidden');
        } else {
            systemInstSection.classList.add('hidden');
        }

        engineeredPromptText.textContent = data.engineered_prompt;
    }

    // =========================================================================
    // 5. Automatic Technique Auditing
    // =========================================================================
    function renderTechniqueAudits(techniques) {
        techniquesList.innerHTML = '';

        if (!techniques || techniques.length === 0) {
            techniquesPlaceholder.classList.remove('hidden');
            return;
        }

        techniquesPlaceholder.classList.add('hidden');
        techniquesList.classList.remove('hidden');

        const verifiedCount = techniques.filter(t => t.status === 'VERIFIED').length;
        techniqueStatusBadge.textContent = `${verifiedCount} Verified at Runtime`;

        techniques.forEach(tech => {
            const box = document.createElement('div');
            box.className = 'technique-box';

            box.innerHTML = `
                <div class="technique-header-row">
                    <span class="technique-name">${escapeHtml(tech.name)}</span>
                    <span class="technique-badge badge-verified">${escapeHtml(tech.status_badge)}</span>
                </div>
                <div class="technique-field">
                    <strong>Why Selected:</strong> ${escapeHtml(tech.why_selected)}
                </div>
                <div class="technique-field">
                    <strong>How Applied:</strong> ${escapeHtml(tech.how_applied)}
                </div>
                <div class="technique-field">
                    <strong>Role in Result:</strong> ${escapeHtml(tech.role_in_result)}
                </div>
                <span class="technique-proof">Proof: ${escapeHtml(tech.runtime_evidence)}</span>
            `;
            techniquesList.appendChild(box);
        });
    }

    // =========================================================================
    // 6. Experiment Notes Audit Log Appender
    // =========================================================================
    function appendToExperimentLog(technique, prompt, response, latency) {
        const empty = sessionLog.querySelector('.empty-log-state');
        if (empty) empty.remove();

        const row = document.createElement('div');
        row.className = 'session-log-row';
        row.innerHTML = `
            <div class="log-q">Technique: <strong>${escapeHtml(technique)}</strong></div>
            <div style="font-size:12.5px; color:var(--color-text-muted); margin-bottom:6px;">Prompt: "${escapeHtml(prompt)}"</div>
            <div class="log-a">${response.slice(0, 240)}${response.length > 240 ? '...' : ''}</div>
            <div style="font-size: 11px; color: var(--color-text-muted); margin-top: 6px;">
                Latency: ${latency.toFixed(2)}s • Saved to promptcraft_experiments.md
            </div>
        `;
        sessionLog.prepend(row);
    }

    function handleExecutionError(err) {
        loadingIndicator.classList.add('hidden');
        responseContent.classList.remove('hidden');
        responseText.innerHTML = `
            <div style="background:var(--color-danger-bg); border:1px solid var(--color-danger-border); color:var(--color-danger); padding:14px; border-radius:var(--radius-md);">
                <strong>Execution Error:</strong> ${escapeHtml(err.message)}. Please verify that promptcraft_web_server.py is running on localhost:8001.
            </div>
        `;
        if (pipelineStatusTag) {
            pipelineStatusTag.className = 'status-pill';
            pipelineStatusTag.style.background = 'var(--color-danger-bg)';
            pipelineStatusTag.style.color = 'var(--color-danger)';
            pipelineStatusTag.textContent = 'Execution Failed';
        }
    }

    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
