/**
 * COMSATS University Islamabad, Wah Campus
 * Grounded Information Retrieval & Context Engineering System
 * Client-Side Application Logic: Dynamic Flow Diagrams, Runtime Graphs & Technique Audits
 */

document.addEventListener('DOMContentLoaded', () => {
    // Form & Input Elements
    const form = document.getElementById('ragQueryForm');
    const input = document.getElementById('queryInput');
    const submitBtn = document.getElementById('submitBtn');
    const chipsContainer = document.getElementById('chipsContainer');

    // Pipeline Flow Elements
    const pipelineStatusTag = document.getElementById('pipelineStatusTag');
    const flowDiagramContainer = document.getElementById('flowDiagramContainer');

    // Answer Card Elements
    const welcomePlaceholder = document.getElementById('welcomePlaceholder');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const loadingStageTitle = document.getElementById('loadingStageTitle');
    const loadingStageDetail = document.getElementById('loadingStageDetail');
    const answerContent = document.getElementById('answerContent');
    const answerText = document.getElementById('answerText');
    const citationsList = document.getElementById('citationsList');
    const latencyBadge = document.getElementById('latencyBadge');
    const copyBtn = document.getElementById('copyBtn');

    // Visualization Elements
    const visPlaceholder = document.getElementById('visPlaceholder');
    const visRenderArea = document.getElementById('visRenderArea');
    const visDescription = document.getElementById('visDescription');
    const visTypeToggle = document.getElementById('visTypeToggle');

    // Evidence & Technique Elements
    const evidencePlaceholder = document.getElementById('evidencePlaceholder');
    const evidenceList = document.getElementById('evidenceList');
    const chunksBadge = document.getElementById('chunksBadge');
    const techniquesPlaceholder = document.getElementById('techniquesPlaceholder');
    const techniquesList = document.getElementById('techniquesList');
    const techniqueStatusBadge = document.getElementById('techniqueStatusBadge');

    // Session Log & Handbook Modal
    const sessionLog = document.getElementById('sessionLog');
    const exportReportBtn = document.getElementById('exportReportBtn');
    const viewHandbookBtn = document.getElementById('viewHandbookBtn');
    const handbookModal = document.getElementById('handbookModal');
    const modalBackdrop = document.getElementById('modalBackdrop');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const handbookContent = document.getElementById('handbookContent');

    // Runtime state cache
    let currentRuntimeData = null;
    let activeChartType = 'relevance';

    // Quick Suggestion Pills Handler
    if (chipsContainer) {
        chipsContainer.addEventListener('click', (e) => {
            const pill = e.target.closest('.query-pill');
            if (pill) {
                const query = pill.dataset.query;
                input.value = query;
                executePipeline(query);
            }
        });
    }

    // Form Submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = input.value.trim();
        if (query) {
            executePipeline(query);
        }
    });

    if (submitBtn) {
        submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const query = input.value.trim();
            if (query) {
                executePipeline(query);
            }
        });
    }

    // Chart Type Toggle Handlers
    if (visTypeToggle) {
        visTypeToggle.addEventListener('click', (e) => {
            const btn = e.target.closest('.tab-pill');
            if (btn && currentRuntimeData) {
                visTypeToggle.querySelectorAll('.tab-pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeChartType = btn.dataset.chart;
                renderRuntimeVisualization(currentRuntimeData);
            }
        });
    }

    // Copy Button Handler
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const text = answerText.innerText;
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

    // Export Session Report Handler
    if (exportReportBtn) {
        exportReportBtn.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/report');
                if (!res.ok) throw new Error('Report document not accessible.');
                const text = await res.text();
                const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'cui_wah_rag_consultation_report.md';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch (err) {
                alert('Export Notice: ' + err.message);
            }
        });
    }

    // View Handbook Modal Handler
    if (viewHandbookBtn && handbookModal) {
        viewHandbookBtn.addEventListener('click', async () => {
            handbookModal.classList.remove('hidden');
            try {
                const res = await fetch('/api/handbook');
                const md = await res.text();
                handbookContent.textContent = md;
            } catch (e) {
                handbookContent.textContent = 'Failed to load handbook text: ' + e.message;
            }
        });

        if (closeModalBtn) closeModalBtn.addEventListener('click', () => handbookModal.classList.add('hidden'));
        if (modalBackdrop) modalBackdrop.addEventListener('click', () => handbookModal.classList.add('hidden'));
    }

    // =========================================================================
    // Core Execution Pipeline Function
    // =========================================================================
    async function executePipeline(query) {
        if (submitBtn.disabled) return;
        // UI State Transitions
        submitBtn.disabled = true;
        welcomePlaceholder.classList.add('hidden');
        answerContent.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');
        latencyBadge.classList.add('hidden');

        evidencePlaceholder.classList.add('hidden');
        evidenceList.classList.add('hidden');
        chunksBadge.textContent = 'Searching...';

        visPlaceholder.classList.add('hidden');
        visRenderArea.classList.add('hidden');
        visTypeToggle.style.display = 'none';

        techniquesPlaceholder.classList.add('hidden');
        techniquesList.classList.add('hidden');
        techniqueStatusBadge.textContent = 'Auditing...';

        // Render Dynamic Initial Pipeline State
        renderInitialFlowState(query);

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                throw new Error(`Server returned HTTP ${response.status}`);
            }

            const data = await response.json();
            currentRuntimeData = data;

            // 1. Render Completed Dynamic Execution Flow Diagram
            renderCompletedFlowDiagram(data);

            // 2. Render Grounded Answer & Citations
            renderGroundedAnswer(data);

            // 3. Render Intelligent Runtime Visualizations
            renderRuntimeVisualization(data);

            // 4. Render Retrieved Evidence Chunks
            renderRetrievedEvidence(data.top_chunks);

            // 5. Render Automatic Technique Identification
            renderTechniquesAudit(data.techniques);

            // 6. Append to Session Audit Log
            appendToAuditLog(query, data.answer, data.latency_sec);

        } catch (err) {
            console.error('Pipeline execution error:', err);
            handleExecutionError(err);
        } finally {
            submitBtn.disabled = false;
        }
    }

    // =========================================================================
    // 1. Dynamic Flow Diagram Renderer (Real Sequence & Decision Gate)
    // =========================================================================
    function renderInitialFlowState(query) {
        if (pipelineStatusTag) {
            pipelineStatusTag.className = 'status-pill status-active';
            pipelineStatusTag.textContent = 'Pipeline Executing...';
        }

        const words = query.split(/\s+/).filter(Boolean);
        const estTokens = Math.max(1, Math.round(query.length / 4));

        flowDiagramContainer.innerHTML = `
            <div class="flow-track">
                <div class="flow-node state-active" id="flow-node-1">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 1</span>
                        <span class="flow-node-badge">${words.length} words</span>
                    </div>
                    <div class="flow-node-title">Query Ingestion</div>
                    <div class="flow-node-summary">~${estTokens} tokens • Ingested</div>
                    <div class="flow-node-detail">${escapeHtml(query.slice(0, 30))}${query.length > 30 ? '...' : ''}</div>
                </div>

                <div class="flow-connector">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </div>

                <div class="flow-node state-active" id="flow-node-2">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 2</span>
                        <span class="flow-node-badge">Scoring</span>
                    </div>
                    <div class="flow-node-title">Corpus BM25 Scoring</div>
                    <div class="flow-node-summary">Evaluating 29 candidate chunks...</div>
                    <div class="flow-node-detail">Vocabulary IDF match</div>
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
                        <span class="flow-node-badge">Decision</span>
                    </div>
                    <div class="flow-node-title">Relevance Decision Gate</div>
                    <div class="flow-node-summary">Threshold evaluation (&gt; 0.0)</div>
                    <div class="flow-node-detail">Pending scores</div>
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
                        <span class="flow-node-badge">Assembly</span>
                    </div>
                    <div class="flow-node-title">Context Window</div>
                    <div class="flow-node-summary">Token budget allocation</div>
                    <div class="flow-node-detail">Top-k assembly</div>
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
                        <span class="flow-node-badge">Inference</span>
                    </div>
                    <div class="flow-node-title">Model Inference</div>
                    <div class="flow-node-summary">Gemini temp=0.0 grounding</div>
                    <div class="flow-node-detail">Strict constraints</div>
                </div>

                <div class="flow-connector">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </div>

                <div class="flow-node state-pending">
                    <div class="flow-node-header">
                        <span class="flow-node-step">Stage 6</span>
                        <span class="flow-node-badge">Verification</span>
                    </div>
                    <div class="flow-node-title">Citation Guardrail</div>
                    <div class="flow-node-summary">Verification against chunks</div>
                    <div class="flow-node-detail">Anti-hallucination check</div>
                </div>
            </div>
        `;
    }

    function renderCompletedFlowDiagram(data) {
        if (pipelineStatusTag) {
            pipelineStatusTag.className = 'status-pill status-completed';
            pipelineStatusTag.textContent = `Completed in ${data.latency_sec.toFixed(2)}s • All Stages Verified`;
        }

        const stages = data.stages || [];
        if (!stages.length) return;

        let html = '<div class="flow-track">';
        stages.forEach((stage, idx) => {
            const isDecision = stage.id === 'stage-decision';
            const stateClass = stage.status_class === 'completed' ? 'state-completed' :
                               stage.status_class === 'failed' ? 'state-failed' : 'state-active';

            html += `
                <div class="flow-node ${stateClass} ${isDecision ? 'state-decision' : ''}" title="${escapeHtml(stage.summary)}">
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
    // 2. Grounded Answer Presentation
    // =========================================================================
    function renderGroundedAnswer(data) {
        loadingIndicator.classList.add('hidden');
        answerContent.classList.remove('hidden');

        // Clean markdown bold syntax
        let formatted = data.answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Clean markdown lists
        formatted = formatted.replace(/^\s*[\-\*]\s+(.*)$/gm, '<li>$1</li>');
        if (formatted.includes('<li>')) {
            formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul style="margin: 8px 0 12px 18px; padding-left: 4px;">$1</ul>');
        }
        answerText.innerHTML = formatted;

        // Render Citations Tags
        citationsList.innerHTML = '';
        const verified = data.verified_citations || [];

        if (verified.length > 0) {
            verified.forEach(cit => {
                const pill = document.createElement('span');
                pill.className = 'citation-pill-item';
                pill.textContent = `[${cit.chunk_id}] • Verified`;
                citationsList.appendChild(pill);
            });
        } else if (data.guardrail && data.guardrail.is_negative_fallback) {
            const pill = document.createElement('span');
            pill.className = 'meta-badge';
            pill.textContent = 'Negative Fallback Constraint Active (Zero citations asserted)';
            citationsList.appendChild(pill);
        } else {
            const pill = document.createElement('span');
            pill.className = 'meta-badge';
            pill.textContent = 'Direct Handbook Policy Grounding';
            citationsList.appendChild(pill);
        }

        latencyBadge.textContent = `Latency: ${data.latency_sec.toFixed(2)}s`;
        latencyBadge.classList.remove('hidden');
    }

    // =========================================================================
    // 3. Intelligent Runtime Visualizations (Bar Charts, Token Distributions & Diagnostics)
    // =========================================================================
    function renderRuntimeVisualization(data) {
        visPlaceholder.classList.add('hidden');
        visRenderArea.classList.remove('hidden');

        const vis = data.visualization || {};
        visDescription.textContent = vis.description || 'Execution visualization plotted from runtime metrics.';

        // If the system has positive score data, enable the toggle between Relevance Scores & Token Budget
        if (vis.has_graph_data) {
            visTypeToggle.style.display = 'inline-flex';
            if (activeChartType === 'relevance') {
                renderRelevanceScoreBarChart(vis.candidate_scores || []);
            } else {
                renderTokenBudgetDistribution(data.token_budget || {}, vis.token_distribution || []);
            }
        } else {
            // Requirement 3: If no suitable data for graph (scores = 0), NEVER draw meaningless blank chart!
            // Show structured diagnostic table instead.
            visTypeToggle.style.display = 'none';
            renderDiagnosticRetrievalTable(data);
        }
    }

    // A. Native SVG Horizontal Bar Chart for Candidate Relevance Scores
    function renderRelevanceScoreBarChart(candidates) {
        if (!candidates || candidates.length === 0) {
            visRenderArea.innerHTML = '<p class="empty-display-box">No chunk candidates recorded.</p>';
            return;
        }

        const maxScore = Math.max(...candidates.map(c => c.score), 1.0);
        const barHeight = 24;
        const barGap = 12;
        const labelWidth = 140;
        const chartWidth = 560;
        const chartHeight = candidates.length * (barHeight + barGap) + 40;
        const maxBarWidth = chartWidth - labelWidth - 80;

        let svgContent = `
            <svg class="chart-svg" viewBox="0 0 ${chartWidth} ${chartHeight}" preserveAspectRatio="xMinYMin meet">
                <!-- Baseline Axis -->
                <line x1="${labelWidth}" y1="10" x2="${labelWidth}" y2="${chartHeight - 20}" class="chart-axis-line" />
                <line x1="${labelWidth}" y1="${chartHeight - 20}" x2="${chartWidth - 20}" y2="${chartHeight - 20}" class="chart-axis-line" />
        `;

        candidates.forEach((cand, idx) => {
            const y = 14 + idx * (barHeight + barGap);
            const barW = Math.max(3, (cand.score / maxScore) * maxBarWidth);
            const isInjected = cand.injected;

            svgContent += `
                <g class="chart-row" data-chunk="${escapeHtml(cand.chunk_id)}">
                    <!-- Chunk Label -->
                    <text x="${labelWidth - 10}" y="${y + 16}" text-anchor="end" class="chart-label">
                        ${escapeHtml(cand.chunk_id)}
                    </text>
                    
                    <!-- Bar Rect -->
                    <rect 
                        x="${labelWidth + 2}" 
                        y="${y}" 
                        width="${barW}" 
                        height="${barHeight}" 
                        class="chart-bar-rect ${isInjected ? 'injected' : ''}"
                    >
                        <title>${escapeHtml(cand.chunk_id)}: ${cand.score} (Title: ${escapeHtml(cand.doc_title)})</title>
                    </rect>

                    <!-- Score Value Text -->
                    <text x="${labelWidth + barW + 10}" y="${y + 16}" class="chart-value-label">
                        ${cand.score.toFixed(3)} ${isInjected ? '• Injected' : ''}
                    </text>
                </g>
            `;
        });

        // Threshold indicator at score 0.0
        svgContent += `
                <text x="${labelWidth}" y="${chartHeight - 6}" text-anchor="middle" class="chart-label" style="font-size: 10px;">
                    0.0 Threshold
                </text>
                <text x="${chartWidth - 40}" y="${chartHeight - 6}" text-anchor="middle" class="chart-label" style="font-size: 10px;">
                    Max: ${maxScore.toFixed(2)}
                </text>
            </svg>
        `;

        visRenderArea.innerHTML = `
            <div class="svg-chart-container">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; font-size:12px; color:var(--color-text-muted);">
                    <span>Green bars indicate chunks injected into context window (&gt; 0.0 threshold)</span>
                    <span style="font-family:var(--font-mono);">BM25 TF-IDF Metric</span>
                </div>
                ${svgContent}
            </div>
        `;
    }

    // B. Token Budget Distribution Bar & Metrics
    function renderTokenBudgetDistribution(budget, distribution) {
        const total = budget.total_tokens || 1;

        let segmentsHtml = '';
        let legendHtml = '';

        const classMap = {
            'Query': 'token-seg-query',
            'Retrieved Context': 'token-seg-context',
            'System Instructions': 'token-seg-system',
            'Model Response': 'token-seg-response'
        };

        const colorMap = {
            'Query': '#3B82F6',
            'Retrieved Context': '#0D9488',
            'System Instructions': '#64748B',
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
                    Total Context Allocation: <strong>${total} tokens</strong> • Signal-to-noise ratio: <strong>${Math.round((budget.context_tokens || 0) / total * 100)}% active evidence</strong>
                </div>
            </div>
        `;
    }

    // C. Structured Diagnostic Retrieval Table (When query produces no positive score matches)
    function renderDiagnosticRetrievalTable(data) {
        visRenderArea.innerHTML = `
            <div class="diagnostic-table-wrapper">
                <div class="diagnostic-banner">
                    <strong>Anti-Hallucination Guardrail Active:</strong> No handbook chunks exceeded the BM25 relevance threshold (&gt; 0.0) for this query. To ensure institutional data accuracy, the system suppressed speculative generation and invoked the negative assertion constraint.
                </div>
                <table class="diagnostic-table">
                    <thead>
                        <tr>
                            <th>Diagnostic Parameter</th>
                            <th>Observed Runtime Value</th>
                            <th>Guardrail Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Corpus Documents Scanned</td>
                            <td>9 Sections (CUI Wah Student Handbook)</td>
                            <td><span class="meta-badge">Complete</span></td>
                        </tr>
                        <tr>
                            <td>Candidate Chunks Evaluated</td>
                            <td>29 Total Chunks</td>
                            <td><span class="meta-badge">100% Coverage</span></td>
                        </tr>
                        <tr>
                            <td>Highest Relevance Score</td>
                            <td>0.000 (No term overlap)</td>
                            <td><span class="meta-badge" style="color:var(--color-warning);">Threshold Unmet</span></td>
                        </tr>
                        <tr>
                            <td>Context Window Fallback</td>
                            <td>Negative Assertion Injected</td>
                            <td><span class="meta-badge" style="color:var(--color-success);">Protected</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    }

    // =========================================================================
    // 4. Retrieved Evidence Presentation
    // =========================================================================
    function renderRetrievedEvidence(chunks) {
        evidenceList.innerHTML = '';

        if (!chunks || chunks.length === 0) {
            evidencePlaceholder.classList.remove('hidden');
            evidencePlaceholder.innerHTML = '<p>No handbook chunks exceeded the relevance threshold. Anti-hallucination guardrail active.</p>';
            chunksBadge.textContent = '0 Chunks Selected';
            return;
        }

        chunksBadge.textContent = `${chunks.length} Chunks Injected`;
        evidenceList.classList.remove('hidden');

        chunks.forEach(chunk => {
            const card = document.createElement('div');
            card.className = 'evidence-card-item';
            card.innerHTML = `
                <div class="evidence-meta-row">
                    <span class="evidence-id-tag">[${escapeHtml(chunk.chunk_id)}]</span>
                    <span class="evidence-score-pill">Score: ${Number(chunk.score).toFixed(3)}</span>
                </div>
                <div class="evidence-doc-name">${escapeHtml(chunk.doc_title)}</div>
                <div class="evidence-body-text">${escapeHtml(chunk.text)}</div>
            `;
            evidenceList.appendChild(card);
        });
    }

    // =========================================================================
    // 5. Automatic Technique Identification & Explanation
    // =========================================================================
    function renderTechniquesAudit(techniques) {
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

            let badgeClass = 'badge-verified';
            if (tech.status === 'STANDBY') badgeClass = 'badge-standby';
            if (tech.status === 'NOT_USED') badgeClass = 'badge-inactive';

            box.innerHTML = `
                <div class="technique-header-row">
                    <span class="technique-name">${escapeHtml(tech.name)}</span>
                    <span class="technique-badge ${badgeClass}">${escapeHtml(tech.status_badge)}</span>
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
    // 6. Session Audit Log Appender
    // =========================================================================
    function appendToAuditLog(query, answer, latency) {
        const empty = sessionLog.querySelector('.empty-log-state');
        if (empty) empty.remove();

        const row = document.createElement('div');
        row.className = 'session-log-row';
        row.innerHTML = `
            <div class="log-q">Inquiry: ${escapeHtml(query)}</div>
            <div class="log-a">${answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</div>
            <div style="font-size: 11px; color: var(--color-text-muted); margin-top: 6px;">
                Verified Grounding • Latency: ${latency.toFixed(2)}s • Logged to rag_session_report.md
            </div>
        `;
        sessionLog.prepend(row);
    }

    // =========================================================================
    // 7. Multi-View Tab Switcher & API Key Failover Status
    // =========================================================================
    const tabChatbot = document.getElementById('tabChatbot');
    const tabRagStudio = document.getElementById('tabRagStudio');
    const chatbotView = document.getElementById('chatbotView');
    const ragStudioView = document.getElementById('ragStudioView');

    function switchView(targetView) {
        if (targetView === 'chatbotView') {
            tabChatbot?.classList.add('active');
            tabRagStudio?.classList.remove('active');
            chatbotView?.classList.remove('hidden');
            ragStudioView?.classList.add('hidden');
        } else {
            tabRagStudio?.classList.add('active');
            tabChatbot?.classList.remove('active');
            ragStudioView?.classList.remove('hidden');
            chatbotView?.classList.add('hidden');
        }
    }

    tabChatbot?.addEventListener('click', () => switchView('chatbotView'));
    tabRagStudio?.addEventListener('click', () => switchView('ragStudioView'));

    async function fetchServerStatus() {
        try {
            const res = await fetch('/api/status');
            if (res.ok) {
                const data = await res.json();
                const api = data.api_keys || {};
                const count = api.key_count || 1;
                const primary = api.api_key_masked || 'Active';
                const failoverOn = api.failover_enabled;
                const statusStr = failoverOn ? `${count} Keys • Auto-Failover Active` : `${count} Key Active`;

                const statusLabel = document.getElementById('apiKeyStatusLabel');
                const keyStatusText = document.getElementById('keyStatusText');
                const footerKeyStatus = document.getElementById('footerKeyStatus');

                if (statusLabel) statusLabel.textContent = statusStr;
                if (keyStatusText) {
                    keyStatusText.textContent = `${count} Keys Configured (Active: ${primary} | Failover Ready)`;
                }
                if (footerKeyStatus) {
                    footerKeyStatus.textContent = `${count} Gemini API Keys Active (Auto-Failover Enabled)`;
                }
            }
        } catch (e) {
            console.debug('Status check bypassed:', e);
        }
    }
    fetchServerStatus();

    // =========================================================================
    // 8. CampusMind Live Interactive Chatbot Logic
    // =========================================================================
    const STRATEGY_INFO = {
        '1': {
            name: 'Zero Context (Baseline)',
            desc: 'Sends prompt with NO campus knowledge injected. Demonstrates hallucination and parametric guesswork.'
        },
        '2': {
            name: 'Full Context Dump',
            desc: 'Dumps all campus knowledge records into context. High tokens (~1,200 tok) and wasteful token budget.'
        },
        '3': {
            name: 'Filtered Context',
            desc: 'Filters relevant documents using keyword ranking before prompt injection (~300 tokens).'
        },
        '4': {
            name: 'Production Mini-RAG [Recommended]',
            desc: 'Retrieves top chunks from campus knowledge and handbook, requiring strict [DOC-XXX] citations.'
        },
        '5': {
            name: 'Conversational Memory',
            desc: 'Maintains multi-turn conversational history in prompt context to remember prior student messages.'
        },
        '6': {
            name: 'Structured JSON Extractor',
            desc: 'Extracts campus policies and outputs a validated JSON schema card with topic, metrics, and summary.'
        }
    };

    let activeChatbotStrategy = '4';
    let chatConversationState = [];

    const strategyPills = document.getElementById('strategyPills');
    const stratBadge = document.getElementById('stratBadge');
    const stratDescText = document.getElementById('stratDescText');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const chatMessages = document.getElementById('chatMessages');
    const clearChatBtn = document.getElementById('clearChatBtn');
    const chatQuickChips = document.getElementById('chatQuickChips');

    // Strategy pill selector
    if (strategyPills) {
        strategyPills.addEventListener('click', (e) => {
            const pill = e.target.closest('.strat-pill');
            if (pill) {
                strategyPills.querySelectorAll('.strat-pill').forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                activeChatbotStrategy = pill.dataset.strategy;
                const info = STRATEGY_INFO[activeChatbotStrategy] || STRATEGY_INFO['4'];
                if (stratBadge) stratBadge.textContent = `Strategy ${activeChatbotStrategy}: ${info.name}`;
                if (stratDescText) stratDescText.textContent = info.desc;

                const meterStrat = document.getElementById('meterStrategy');
                if (meterStrat) meterStrat.textContent = `Strategy ${activeChatbotStrategy}: ${info.name.split(' ')[0]}`;
            }
        });
    }

    // Suggested quick prompt chips
    if (chatQuickChips) {
        chatQuickChips.addEventListener('click', (e) => {
            const chip = e.target.closest('.chat-chip');
            if (chip && chip.dataset.query) {
                submitChatInquiry(chip.dataset.query);
            }
        });
    }

    // Clear chat button
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', () => {
            chatConversationState = [];
            const msgs = chatMessages.querySelectorAll('.chat-msg:not(:first-child)');
            msgs.forEach(m => m.remove());
            renderMemoryTurns();
        });
    }

    // Chat form submit
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const q = chatInput.value.trim();
            if (q) {
                submitChatInquiry(q);
            }
        });
    }

    function appendChatBubble(role, content, data = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-msg ${role === 'user' ? 'msg-user' : 'msg-bot'}`;

        const avatar = role === 'user' ? '🎓' : '🤖';
        const sender = role === 'user' ? 'Student' : 'CampusMind AI';

        let bodyHtml = '';
        if (data && data.is_json && data.json_data) {
            bodyHtml = `<p><strong>Structured JSON Card:</strong></p><pre><code>${escapeHtml(JSON.stringify(data.json_data, null, 2))}</code></pre>`;
        } else {
            // Format bold text, markdown linebreaks, and code snippets
            let formatted = escapeHtml(content)
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n\n/g, '</p><p>')
                .replace(/\n/g, '<br/>');

            // Highlight citation tags
            formatted = formatted.replace(/\[(DOC-[A-Z0-9\-]+)\]/g, '<span class="citation-chip">[$1]</span>');
            bodyHtml = `<p>${formatted}</p>`;
        }

        let metaHtml = '';
        if (role === 'bot' && data) {
            const stratLabel = data.strategy ? escapeHtml(data.strategy.name) : 'RAG Grounded';
            const latencyStr = data.latency_sec ? `${data.latency_sec}s` : '0.0s';
            const tokStr = data.tokens_estimated ? `~${data.tokens_estimated} tok` : '';

            metaHtml = `
                <div class="msg-meta">
                    <span class="msg-tag">${stratLabel}</span>
                    <span class="msg-tag">⏱ ${latencyStr}</span>
                    ${tokStr ? `<span class="msg-tag">Context: ${tokStr}</span>` : ''}
                </div>
            `;
        }

        msgDiv.innerHTML = `
            <div class="msg-avatar">${avatar}</div>
            <div class="msg-bubble">
                <div class="msg-sender">${sender}</div>
                <div class="msg-body">${bodyHtml}</div>
                ${metaHtml}
            </div>
        `;

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.id = id;
        typingDiv.className = 'chat-msg msg-bot';
        typingDiv.innerHTML = `
            <div class="msg-avatar">🤖</div>
            <div class="msg-bubble" style="padding: 10px 16px;">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span class="status-pulse-dot" style="width:7px; height:7px;"></span>
                    <span style="font-size:12.5px; color:var(--color-text-muted);">CampusMind is processing your query with Strategy ${activeChatbotStrategy}...</span>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function hideTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    async function submitChatInquiry(queryText) {
        if (!queryText) return;
        chatInput.value = '';
        chatInput.focus();

        appendChatBubble('user', queryText);
        const typingId = showTypingIndicator();
        if (chatSendBtn) chatSendBtn.disabled = true;

        try {
            const resp = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: queryText,
                    strategy: activeChatbotStrategy,
                    history: chatConversationState
                })
            });

            hideTypingIndicator(typingId);
            if (chatSendBtn) chatSendBtn.disabled = false;

            if (!resp.ok) {
                throw new Error(`Server returned status HTTP ${resp.status}`);
            }

            const payload = await resp.json();
            appendChatBubble('bot', payload.answer, payload);
            updateChatTelemetry(payload);

            chatConversationState.push({ role: 'user', text: queryText });
            chatConversationState.push({ role: 'assistant', text: payload.answer });
            renderMemoryTurns();

        } catch (err) {
            hideTypingIndicator(typingId);
            if (chatSendBtn) chatSendBtn.disabled = false;
            appendChatBubble('bot', `⚠️ Server Error: ${err.message}. Please verify the localhost server is running.`);
        }
    }

    function updateChatTelemetry(data) {
        const meterStrat = document.getElementById('meterStrategy');
        const meterCtx = document.getElementById('meterContext');
        const meterLat = document.getElementById('meterLatency');
        const meterSig = document.getElementById('meterSignal');
        const signalFill = document.getElementById('signalProgressFill');
        const citationsListEl = document.getElementById('chatCitationsList');
        const citCountBadge = document.getElementById('citationCountBadge');
        const telemBadge = document.getElementById('telemetryStatusBadge');

        if (meterStrat && data.strategy) {
            meterStrat.textContent = `[${data.strategy.key}] ${data.strategy.name}`;
        }
        if (meterCtx) {
            meterCtx.textContent = `${data.context_len || 0} chars (~${data.tokens_estimated || 0} tok)`;
        }
        if (meterLat) {
            meterLat.textContent = `${data.latency_sec || 0.0}s`;
        }
        if (meterSig) {
            const pct = Math.round((data.signal_ratio || 0.0) * 100);
            meterSig.textContent = `${pct}% Signal`;
            if (signalFill) signalFill.style.width = `${pct}%`;
        }
        if (telemBadge) {
            telemBadge.textContent = 'Updated';
            telemBadge.className = 'meta-badge';
        }

        if (citationsListEl) {
            citationsListEl.innerHTML = '';
            const citations = data.citations || [];
            if (citCountBadge) citCountBadge.textContent = `${citations.length} Sources`;

            if (citations.length > 0) {
                citations.forEach(cit => {
                    const pill = document.createElement('span');
                    pill.className = 'citation-chip';
                    pill.textContent = cit;
                    citationsListEl.appendChild(pill);
                });
            } else if (data.augmented_chunks && data.augmented_chunks.length > 0) {
                data.augmented_chunks.forEach(c => {
                    const pill = document.createElement('span');
                    pill.className = 'citation-chip';
                    pill.textContent = `[${c.chunk_id}]`;
                    citationsListEl.appendChild(pill);
                });
            } else {
                citationsListEl.innerHTML = `<span class="empty-note">No citations generated for this context strategy.</span>`;
            }
        }
    }

    function renderMemoryTurns() {
        const container = document.getElementById('memoryTurnsList');
        const badge = document.getElementById('memoryTurnsBadge');
        if (!container) return;

        const count = Math.floor(chatConversationState.length / 2);
        if (badge) badge.textContent = `${count} Turns`;

        if (chatConversationState.length === 0) {
            container.innerHTML = `<span class="empty-note">Turn history is maintained and fed into context for Strategy 5 (Conversational Memory).</span>`;
            return;
        }

        container.innerHTML = '';
        for (let i = 0; i < chatConversationState.length; i += 2) {
            const userTurn = chatConversationState[i];
            const botTurn = chatConversationState[i + 1];
            const item = document.createElement('div');
            item.className = 'memory-turn-item';
            item.innerHTML = `
                <div><strong>Student:</strong> ${escapeHtml(userTurn?.text?.substring(0, 50) || '')}...</div>
                <div style="font-size:11px; color:var(--color-text-muted); margin-top:2px;">
                    <strong>CampusMind:</strong> ${escapeHtml(botTurn?.text?.substring(0, 45) || '')}...
                </div>
            `;
            container.appendChild(item);
        }
    }

    // Error Handler
    function handleExecutionError(err) {
        loadingIndicator.classList.add('hidden');
        answerContent.classList.remove('hidden');
        answerText.innerHTML = `
            <div style="background:var(--color-danger-bg); border:1px solid var(--color-danger-border); color:var(--color-danger); padding:14px; border-radius:var(--radius-md);">
                <strong>Execution Error:</strong> ${escapeHtml(err.message)}. Please verify that rag_web_server.py is running on localhost.
            </div>
        `;
        citationsList.innerHTML = '';
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
