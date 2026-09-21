---
title: "Developing an Interactive TNM Staging Tool for Otolaryngology Education"
date: "2025-12-14"
slug: "staging-dojo"
description: "Building Staging Dojo: an interactive TNM staging trainer and a reflection on deliberate practice in medical education."
original_url: "https://chrishornung14.medium.com/developing-an-interactive-tnm-staging-tool-for-otolaryngology-education-0def72b244c7"
original_note: "Originally published on Medium."
---

[Link to App](https://oral-cavity-staging-ninja.vercel.app/quiz)

**The CrabsMcChaffey Staging Dojo**

<figure>
<img src="/blog/assets/staging-dojo/staging-dojo-december-2025.webp" alt="CrabsMcChaffey Staging Dojo TNM staging practice interface as shown in December 2025" loading="lazy">
<figcaption>Screenshot of the CrabsMcChaffey Staging Dojo 12/2025</figcaption>
</figure>

### During my PGY-2 year, I realized I was doing something ridiculous.

I would sit down with the AJCC book or Pocket Guide, tell myself I was going to “review staging,” read through the head and neck section, and then never actually test whether I could apply any of it.

If you are in ENT, you probably know the pattern. Oral cavity staging is a tangle of size, depth of invasion, bone involvement, and nodal disease. Oropharynx splits into different systems depending on HPV status. Nasopharynx has its own rules. The N categories are their own small circus.

You can read the tables enough times that they start to look familiar. Then somebody asks you to stage an actual patient and you are back to flipping pages.

I wanted something that felt more like ABG Ninja for head and neck cancer, so I built it.

The first version was pretty simple: an interactive TNM staging trainer focused on oral cavity cancer. You got a case, committed to a T category, N category, and stage group, and immediately found out whether you were right. I called it Staging Dojo.

What I did not expect was that this small side project would change how I think about medical education and eventually become a template for several other educational tools.

## The problem wasn’t access to information

There is no shortage of information about TNM staging. The staging manuals exist. Pocket guides exist. There are tables, review articles, lectures, flashcards, and probably several PDFs buried somewhere on every ENT resident’s phone.

The problem, at least for me, was that reading those resources was not the same thing as being able to stage a patient.

Staging sits at an annoying intersection. It is testable on in-service and board examinations, matters clinically for prognosis and treatment planning, and is remarkably difficult to learn passively from a table. What I actually needed was not another explanation of oral cavity staging. I needed someone to hand me 30 oral cavity cancers and make me stage them.

The learning loop I wanted was pretty straightforward:

1. Get a case.
2. Extract the relevant information.
3. Commit to an answer.
4. Find out whether you were right.
5. Understand why.
6. Do it again.

That is essentially what happens in clinic and tumor board, except clinical exposure is unpredictable. You cannot order up five T2 oral tongue cancers, three weird necks, and a case with extranodal extension because those happen to be the things you need to practice that day.

Software can.

That became the basic idea behind Staging Dojo.

## Start small enough that you actually build something

One of the better decisions I made was deliberately making the first version small. Head and neck staging is enormous. I could have started by trying to build oral cavity, HPV-positive oropharynx, HPV-negative oropharynx, larynx, hypopharynx, nasopharynx, nasal cavity, and paranasal sinus staging simultaneously. I probably would still be working on version 0.1.

Instead, I started with oral cavity. Even then, I wanted the cases to feel like patients rather than generic board questions, so I divided them across actual subsites: oral tongue, floor of mouth, alveolar ridge, buccal mucosa, hard palate, and retromolar trigone.

The goal was not to build a comprehensive medical education platform. It was to make one thing useful.

Once that worked, expansion became much easier. Staging Dojo now includes substantially more of head and neck cancer staging, with separate logic and cases for different disease sites. The architecture that started with oral cavity turned out to be reusable.

That lesson has carried into essentially every educational project I have built since: **build the smallest version that solves the actual problem, then expand it.**

## Commit first, then compare

As I used the Dojo more, I realized that the most important part of the interface was not actually the staging algorithm. It was the fact that the learner had to commit to an answer.

There is an enormous difference between reading that a 2.5-cm oral tongue tumor with 8 mm depth of invasion is T2 and being given the case, selecting T2, and pressing submit. The first feels familiar. The second tests whether you actually know it.

This is also how I increasingly try to learn clinically. If I am evaluating a cancer patient, I try to stage the cancer myself before looking up the answer or discussing it with someone more experienced. If I am thinking through management, I try to decide what I would do before hearing the attending’s plan.

Being wrong is useful when you have committed to something because it gives you an error to examine. That became one of the central principles of the Dojo format: **commit first, then compare.**

The software is really just a way to manufacture that experience repeatedly.

## Immediate feedback matters

The second principle was feedback. A red box telling you that you selected the wrong stage is not particularly educational. The useful question is: **why was I wrong?**

So each case needs an explanation. Sometimes that explanation is simple. Sometimes it is the edge case that makes the question worth asking in the first place: depth of invasion, extranodal extension, laterality, number of nodes, invasion of a particular structure, or one of the many exceptions that makes head and neck staging so enjoyable.

This turned out to be one of the most time-consuming parts of building the project. Writing code is relatively fast. Writing a large number of clinically realistic cases that test different concepts without simply repeating the same pattern is much harder.

It is also probably where most of the educational value lives.

## Encoding a staging system teaches you the staging system

One of the unexpected benefits of building Staging Dojo was what happened when I tried to translate staging tables into code. A staging table can hide ambiguity surprisingly well. Code cannot.

At some point, the computer needs an explicit answer: if these clinical features are true, what stage is it?

When you start translating a staging system into explicit rules, edge cases become painfully obvious. You notice where two rules intersect. You realize which variables actually determine the answer. You find assumptions you did not realize you were making.

I learned staging while building a tool intended to teach staging.

That has become one of my favorite things about programming as a physician. Turning clinical knowledge into software forces you to define your mental model precisely enough that a computer can execute it. If you cannot explain the rule clearly enough to encode it, there is a decent chance you do not understand the rule as well as you think you do.

## Separate the content from the engine

The original version of Staging Dojo was built with Next.js and TypeScript. The cases lived in structured files, the staging rules lived in separate functions, and the interface handled presenting questions and collecting answers.

At the time, separating those pieces mostly felt like good programming hygiene. It turned out to matter quite a bit as the project grew.

If the cases, staging rules, and user interface are all tangled together, every expansion becomes a rewrite. If they are separated, adding a new disease site becomes much more manageable: define the relevant clinical inputs, encode and test the staging rules, build a case bank, and plug it into the existing interface.

The same principle applies beyond staging. Once the educational interaction is separated from the content being taught, the software starts becoming reusable.

That was the point where Staging Dojo stopped being just a staging website and started giving me ideas for other tools.

## The “Dojo” became a format

Somewhere along the way, Dojo became my shorthand for a particular kind of educational tool. The content can change, but the basic philosophy stays the same: **give the learner realistic cases, make them commit to a decision, provide immediate and useful feedback, and then give them another rep.**

That architecture is particularly appealing for parts of medicine that are difficult to learn through passive review. Staging is an obvious example, but it is certainly not the only one.

I have since started applying the same concept to Mohs reconstruction. That problem is different from TNM staging because there is not always an equation that takes a defect and spits out the “correct” reconstruction. Instead, the learner has to integrate location, size, depth, surrounding tissue, functional considerations, and reconstructive options. That makes it an interesting test of whether the Dojo format can extend beyond classification systems into areas involving more clinical and surgical judgment.

More recently, I started building a TI-RADS Dojo around thyroid ultrasound. Again, the content is different, but the educational problem is familiar. You can read the TI-RADS criteria, or you can look at thyroid nodules, identify the relevant features, assign points, commit to a category, and get feedback.

I would rather do the second.

The more of these projects I build, the more I think there is a broad category of medical knowledge that lends itself to this approach.

## Build the reps

Medicine still relies heavily on opportunistic learning. You learn from the patients who happen to come through the door, and that is obviously indispensable. No software tool replaces taking care of actual patients.

But clinical exposure has limitations as a learning system. The cases are not balanced. Rare but important scenarios are rare. You may see the same straightforward problem twenty times and encounter a particular edge case once during residency. The patient in front of you also exists to receive care, not to complete your curriculum.

Educational software gives us a way to supplement that experience. If I need more practice recognizing a particular staging pattern, I do not necessarily need to wait six months until another patient with that pattern appears. I can manufacture the reps.

That is increasingly how I think about these tools. They are not replacements for textbooks, lectures, attendings, tumor boards, or patients. They are practice environments.

A dojo.

## Then comes the uncomfortable question: does any of this actually work?

There is an obvious problem with building an educational tool for yourself: I like using it, but that does not mean it works.

It is very easy to build something, enjoy using it, show it to a few friends who say it is cool, and conclude that you have improved medical education. That is not evidence.

So the next phase of this project has been moving from software development into medical education research. I am now formally evaluating whether this style of case-based, feedback-rich practice produces measurable improvements in staging performance compared with more traditional educational material.

That transition has changed how I think about building educational software. If you are only building an app, a case needs to look good and return the right answer. If you are trying to study whether the app teaches, suddenly you have much harder questions.

Are the cases balanced? Are the assessments actually measuring staging ability? Are two assessment forms comparable? Are the explanations clinically accurate? Is improvement caused by the educational intervention or simply by taking another staging test? Does the software reliably capture what participants actually did?

The research side has forced a level of rigor that has ultimately made the educational tool itself better. It has also reinforced an important distinction: **building an educational tool and demonstrating that it is educational are two different projects.**

## AI made this possible — but it did not make it automatic

There is another part of this story that would be dishonest to leave out: I am an otolaryngology resident, not a software engineer.

A few years ago, most of these projects probably would have remained ideas in a Notes app. Modern AI coding tools dramatically lowered the barrier between “I wish this existed” and “I can build a prototype of this.”

I can describe the behavior I want, generate scaffolding, ask questions when I do not understand the code, debug errors, and gradually learn enough of the underlying system to modify it myself. That is an extraordinary capability.

It also creates an extraordinary number of ways to be confidently wrong.

A language model can write a beautiful staging function that contains an incorrect staging rule. It can generate a plausible teaching explanation that is clinically false. It can create twenty cases that look varied while accidentally testing the same concept twenty times. The computer does not know that the output matters because someone may use it to learn medicine.

That responsibility still belongs to the person building the tool.

For me, AI has been most useful not as a substitute for knowing the medicine, but as leverage for turning medical knowledge into something functional. The easier software becomes to create, the more important content expertise and validation become.

## What I have learned so far

The original version of Staging Dojo taught me a lot about Next.js, TypeScript, testing, and deployment. The larger project has taught me something more interesting.

There are many areas of medical education where the bottleneck is not information. The information already exists. The bottleneck is **practice**.

Classification systems, imaging interpretation, staging, reconstruction, treatment decisions, anatomy, and pattern recognition are all examples. We frequently teach these things by giving learners information and hoping that clinical exposure eventually provides enough opportunities to apply it.

Sometimes it does. Sometimes we can do better.

I started Staging Dojo because I wanted a better way to memorize TNM staging.

I do not think that is really what I am building anymore.

The more interesting question is whether small, focused educational tools can turn parts of medical training that we traditionally learn through passive review into opportunities for deliberate practice. There are countless skills in medicine that fit that pattern, and many are currently learned by reading about them and then waiting until the right patient happens to appear.

Software gives us another option.

**We can manufacture the reps.**

That is the idea I want to keep exploring.

Find me

[LinkedIn](https://www.linkedin.com/in/chris-hornung/), [X](https://twitter.com/ChrisHornung), [Google Scholar](https://scholar.google.com/citations?user=OwZi2MoAAAAJ&hl=en)
