# The Project Is the Benchmark

## What a 232x GPU optimization result reveals about the future of agent-run work

In June 2026, a developer named Sankalp entered an unusual GPU programming contest. The assignment was to implement a batched QR decomposition, the kind of numerical routine whose practical performance depends on details most software developers can safely spend a career avoiding: Householder reflections, memory movement, launch overhead, precision tolerances, kernel specialization, and the peculiar appetite of tensor cores for matrix-shaped work.

The contest was organized by GPU Mode with Core Automation. Its infrastructure made the problem unusually legible to an agent. A command-line tool could submit a candidate, check its correctness, benchmark it across multiple matrix shapes, and return shape-specific timings. Incorrect implementations were rejected. Correct implementations were ranked by their geometric mean runtime. The problem had a strict contract, a quantitative objective, and a machine-readable verdict.

Sankalp used Codex to work inside that environment. The result was a final tracked runtime of 1,805 microseconds, compared with a rough baseline of 419,000 microseconds: a 232-fold speedup. He placed twelfth among 183 participants despite describing himself as an experienced enthusiast rather than a professional GPU-kernel engineer. The developer immediately above him on the leaderboard was a principal engineer at NVIDIA.

The number is spectacular. The process behind it is more consequential.

According to [Sankalp’s account of the experiment](https://sankalp.bearblog.dev/autoresearch/), Codex made more than 1,500 submissions over fourteen days. It wrote implementations, submitted them, read the timings, profiled bottlenecks, revised the code, preserved promising branches, and tried again. Some goal-directed runs continued for more than a day. The surrounding harness kept a log of accepted and rejected ideas so that later sessions would not have to rediscover the same failures.

This was not quite a machine working in a hermetically sealed room. Sankalp supplied the original problem framing, learned enough of the mathematics to ask better questions, checked in every few hours during parts of the contest, and intervened when the search settled into local maxima. Near the end, those interventions mattered. Progress below roughly 3,000 microseconds required more conceptual steering, more profiling, and more deliberate variation among candidate strategies.

That qualification does not diminish the result. It identifies what was actually invented. The breakthrough was not merely that a language model could write an unusually fast kernel. It was the construction of an environment in which an agent could conduct a sustained empirical search.

The harness converted performance engineering into an operational loop:

> propose, execute, verify, measure, diagnose, revise, and retain what was learned.

Once that loop existed, the model’s capacity to generate code became only one component. The larger capability came from the relationship between a bounded problem, executable tools, quantitative feedback, persistent memory, and permission to continue.

The lesson reaches far beyond CUDA.

## From code generation to project operation

Most discussion about coding agents still concentrates on the artifact they produce. Can the model write the function? Can it repair the test? Can it generate a pull request? These are useful questions, but they preserve the mental model of an assistant waiting for a human to specify the next action.

The kernel experiment suggests a different unit of automation. The unit is not a line of code or even a task. It is a closed learning process.

Many forms of work can be expressed as a search through possible solutions. Software performance makes this obvious because runtime supplies a clean numerical score. Yet product design, editorial work, research, operations, and business development also involve candidates, constraints, observations, and selection. Their evaluators are messier, and some outcomes cannot be established without human participation, but the underlying structure remains recognizable.

A user-interface agent can generate several interaction models, render each one, inspect browser states, test keyboard access, compare visual regressions, and preserve the strongest candidate. An editorial agent can draft competing structures, check every factual claim against sources, measure redundancy and reading complexity, conduct adversarial reviews, and revise the piece. An operational agent can propose a workflow, simulate load and failure conditions, inspect cycle time, identify bottlenecks, and test a revised process. A research agent can maintain competing hypotheses, gather evidence, record negative results, and direct the next experiment toward the most consequential uncertainty.

In each case, the quality of the output depends on more than the model. It depends on whether the project has made success observable.

This is where many agentic projects fail. They automate production before formalizing judgment. The agent can generate a great deal of material, but the system cannot distinguish progress from motion. A test suite can establish that software behaves according to its specification. It cannot establish that the specification serves the intended person. A visual similarity score can detect an accidental layout change. It cannot decide whether the original layout expressed the right hierarchy. A conversion metric can show that more people completed an action. It cannot, by itself, tell us whether the action was informed, manipulative, or valuable.

The benchmark must therefore be larger than the artifact.

## Intent before tickets

A project capable of autonomous iteration needs a governing layer above its backlog. It needs an explicit account of what the project is trying to cause, who or what it serves, which qualities must survive implementation, what evidence can support a success claim, and who has authority to change those definitions.

Without this layer, the issue tracker quietly becomes the strategy. Agents optimize whatever has been rendered most legible: passing tests, closing tickets, reducing latency, increasing clicks, or satisfying the latest instruction. These objectives may be useful, but each is a proxy. Left ungoverned, a sufficiently persistent agent will discover the distance between the proxy and the purpose.

A project engine begins by separating intent from work. Intent defines the durable boundary. Epics and issues decompose that intent into executable units. Each unit carries an objective, dependencies, acceptance criteria, evidence requirements, permissions, exclusions, budgets, and stop conditions. Documentation preserves institutional memory. Tickets represent current operational state. Evidence connects what was done to what may honestly be claimed.

The operational agent then behaves less like an omniscient manager and more like a coordinator with constrained authority. It reconciles the project state, selects a Ready issue, checks dependencies, creates a time-bounded claim on the relevant workspace, assembles the minimum sufficient context, and dispatches a worker. Overlapping write claims are rejected. Read-only investigations can coexist. Expired claims cannot authorize further work. Every release remains in the execution history.

This machinery may sound bureaucratic when applied to a single kernel. At project scale, it becomes the condition that makes autonomy safe enough to be useful. An agent cannot be permitted to reinterpret the project every time it encounters resistance. Nor can several agents be allowed to modify the same conceptual or technical territory without a visible ownership model. The system needs to know which decisions are local, which are reversible, and which require promotion authority.

## The evaluation contract

Sankalp’s kernel loop worked because correctness and speed were both executable. A candidate that returned the wrong decomposition could not compensate with a faster runtime. Among candidates that satisfied the mathematical checker, the benchmark selected the faster implementation.

Every autonomous project loop needs an equivalent evaluation contract, but the contract must match the domain. Software may require unit tests, integration tests, security checks, runtime measurements, and browser evidence. Interface work may add interaction-state coverage, accessibility checks, design-system conformance, visual inspection, and observed use. Editorial work may require source verification, structural review, legal or sensitivity review, and audience testing. Research may require reproducibility, provenance, uncertainty estimates, and independent evaluation.

These forms of evidence are not interchangeable. A system should distinguish among work that is documented, implemented, tested, and empirically validated. A candidate may be fully implemented and pass every automated check while its effect on people remains unknown. Preserving that distinction is not ceremonial caution. It prevents synthetic evidence from laundering itself into a claim about the world.

The evaluator also needs relative independence from the candidate generator. If the same agent can modify the artifact, rewrite the criteria, and approve promotion in one uninterrupted action, failure becomes negotiable. The loop may continue producing cleaner explanations for why its current output should count as success. Stable criteria, explicit authority, and retained evidence make that maneuver visible.

## Escaping the local maximum

The most revealing portion of the kernel account arrives after the easy gains. Codex rapidly reduced the runtime, but later iterations began circling small variations of the same ideas. Sankalp responded by keeping a beam of several candidates alive, encouraging ambitious structural changes, consulting stronger advisor models, clearing stale context, and steering experiments toward bottlenecks revealed by multiple profilers.

This is a general project problem. Optimization tends to improve what the current model of the problem can already see. The better the loop becomes at exploiting its known evaluation surface, the more likely it is to settle into a locally coherent answer whose hidden assumptions remain untouched.

The remedy is deliberate epistemic stress testing.

After a candidate qualifies against its known contract, the project freezes it. A separate evaluator then reveals a previously sealed change in conditions, a World Card, designed to test an assumption the candidate was not optimized to satisfy. A dependency may disappear. Available time may collapse. A different affected person may enter the analysis. Evidence may become contradictory. The original team may no longer be present. A system designed for one hundred records may have to account for one hundred million. Two legitimate intentions, such as privacy and personalization, may collide.

These are designed perturbations rather than random disruptions. Each preserves the project’s protected invariants while changing a controlled part of the world around the candidate. The purpose is to ask a precise question: what must remain true for this result to remain good?

The resulting disposition is more informative than a binary pass or fail. A candidate may be robust and continue to qualify unchanged. It may be adaptable through a bounded correction. It may remain valid only within a narrower domain. It may prove fragile under a plausible condition, unsafe because it crosses a protected invariant, or unknown because the available evaluation cannot support a conclusion.

This method gives formal shape to an activity good teams already perform unevenly through criticism, pre-mortems, red teams, design reviews, and experienced intuition. By giving perturbations a budget, an owner, a reveal gate, and a retained result, the project can direct attention toward unknown variables instead of repeatedly demonstrating what it already knows.

## Memory is part of the machine

An agentic loop without memory is condemned to perform intelligence as repetition. Sankalp’s `log.md` recorded which kernel ideas had succeeded, which had failed, and how each shape responded. As the search became harder, that record became more valuable. Later sessions could begin from accumulated evidence rather than from a polished summary that omitted the dead ends.

At project scale, this memory needs several forms. Operational memory records current issues, claims, dependencies, and state transitions. Institutional memory records intent, architecture, design reasoning, policies, and decisions. Negative-result memory preserves failed experiments and the conditions under which they failed. An unknown-variable ledger records what is controlled, unresolved, assumed but untested, observed only once, discovered through perturbation, or currently unknowable.

Together, these records change the economics of agent work. A new worker does not need every prior conversation. It needs a bounded context packet assembled from authoritative sources: the current issue, governing intent, relevant decisions, active constraints, known failures, required evidence, permissions, and stop conditions. The project, rather than the chat transcript, becomes the durable mind.

## The human role moves upward

It is tempting to describe the kernel result as evidence that the human can be removed from the loop. The actual record supports a more useful conclusion. Human work moves from performing every iteration to designing and governing the system in which iteration occurs.

Sankalp chose the problem, established the harness, learned the domain, shaped the instructions, inspected the evidence, introduced candidate diversity, and intervened when the search lost conceptual range. Codex supplied extraordinary persistence and implementation capacity inside that structure. Neither contribution is well described by the old division between a person who thinks and a tool that executes.

For general projects, the human role increasingly concerns intent, taste, legitimacy, and consequence. People decide which outcomes deserve optimization, which tradeoffs are acceptable, which affected perspectives must be represented, what kinds of evidence count, and which actions require consent. Agents can manage much of the resulting operation, including decomposition, execution, measurement, documentation, and repeated experimentation. The strongest systems will make that division explicit instead of hiding it behind the language of assistance.

This also clarifies where autonomy should stop. External publication, spending, irreversible deletion, legal commitments, communication in another person’s name, and claims about human outcomes may require specific authority. The coordinator should halt when evidence is missing, permissions are ambiguous, protected invariants are threatened, or the next action would create an unauthorized consequence. A stop is a valid project result, not an agent failure.

## The project becomes a learning instrument

The 232x speedup matters because it demonstrates the amount of search that becomes practical when implementation, execution, and measurement are joined in a persistent loop. Its broader significance lies in the architecture around that search.

Once a project can state its intent, represent work as contracts, coordinate bounded agents, evaluate candidates independently, introduce designed perturbations, preserve negative results, and promote only what its evidence supports, the project itself becomes an executable learning system.

The loop improves more than the artifact. It improves the project’s model of its own reality. Each iteration can reveal a faster implementation, a clearer interface, a stronger argument, a safer workflow, or a better experiment. Just as importantly, it can reveal where the current answer stops working, which assumption was carrying more weight than anyone realized, and which question the existing evidence still cannot answer.

That is the transferable idea behind the kernel result. The future of agentic work will not be secured by asking models to produce larger volumes of finished material. It will come from building projects that can tell the difference between an output, an improvement, and a justified decision.

In that environment, the benchmark is no longer a final test attached to the work. The project is the benchmark.

## Origin and further reading

- Sankalp, [“Auto-research with Codex: How I achieved a 232x Faster Kernel over baseline”](https://sankalp.bearblog.dev/autoresearch/), July 8, 2026.
- Machuca Valley Tech, [“The 232x Leap: How AI is Solving the ‘Nuclear Waste’ of Coding”](https://www.machucavalley.tech/blog/auto-research-codex-gpu-kernel-optimization/), August 16, 2026.
- RightNow AI, [AutoKernel](https://github.com/RightNow-AI/autokernel), an open-source autoresearch system for generating optimized Triton kernels from PyTorch models.
