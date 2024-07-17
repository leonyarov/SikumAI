import React from 'react';
import {Box, Typography} from "@mui/material";
import Markdown from "react-markdown";

const data = {
    "bagrut": "**Question 1:**\nAnalyze the literary device of foreshadowing as employed in the opening scene of \"The Master and Margarita\" by Mikhail Bulgakov. How does the author create a sense of foreboding and suspense from the outset, and what does this foreshadow about the events to come?\n\n**Question 2:**\nExamine the character of Professor Woland in Book One of \"The Master and Margarita.\" Discuss his enigmatic nature, his connection to the supernatural, and the possible interpretations of his role as a representative of good or evil. How does his presence disrupt the preconceived notions of the characters and challenge the boundaries of reality in the novel?",
    "book_name": "master_margarita",
    "discussion": "1. What is the main premise of Ivan Nikolayich Bezdomny's poem?\n2. Who is the mysterious foreigner that appears at Patriarch's Ponds?\n3. What does the foreigner reveal to the editor and the poet about Jesus's existence?",
    "reading": "Early in the morning on the fourteenth of the spring month of Nisan the\nProcurator of Judaea, Pontius Pilate, in a white cloak lined with blood-red,\nemerged with his shuffling cavalryman's walk into the arcade connecting the\ntwo wings of the palace of Herod the Great.\nMore than anything else in the world the Procurator hated the smell of\nattar of roses. The omens for the day were bad, as this scent had been\nhaunting him since dawn.\nIt seemed to the Procurator that the very cypresses and palms in the\ngarden were exuding the smell of roses, that this damned stench of roses was\neven mingling with the smell of leather tackle and sweat from his mounted\nbodyguard.\nA haze of smoke was drifting towards the arcade across the upper\ncourtyard of the garden, coming from the wing at the rear of the palace, the\nquarters of the first cohort of the XII Legion ; known as the ' Lightning',\nit had been stationed in Jerusalem since the Procurator's arrival. The same\noily perfume of roses was mixed with the acrid smoke that showed that the\ncenturies' cooks had started to prepare breakfast.\n'Oh gods, what are you punishing me for? . . . No, there's no doubt, I\nhave it again, this terrible incurable pain . . . hemicrania, when half the\nhead aches . . . there's no cure for it, nothing helps. ... I must try not\nto move my head. . . . '\nA chair had already been placed on the mosaic floor by the fountain;\nwithout a glance round, the Procurator sat in it and stretched out his hand",
    "writing": "**Question:**\n\nAnalyze the encounter between Mikhail Alexandrovich Berlioz, Ivan Nikolayich Poniryov, and the mysterious foreigner at Patriarch's Ponds in Chapter 1 of \"The Master and Margarita\" by Mikhail Bulgakov. Consider the characters' initial perceptions, the themes of mortality and destiny, and the role of the supernatural in the novel's opening scene."
}

function LessonPlan({lesson}) {
    // const lesson = data
    return (
        <Box>
            <Typography variant={'h3'} gutterBottom>
                Lesson Plan
            </Typography>
            <Typography variant={'h4'}>
                Reading
            </Typography>

            <Typography variant={'body2'} sx={{overflowWrap: 'break-word'}}>
                <Markdown>
                    {lesson.reading}
                </Markdown>
            </Typography>

            <Typography variant={'h4'}>
                Bagrut Questions
            </Typography>
            <Typography variant={'body2'} sx={{overflowWrap: 'break-word'}}>
                <Markdown>

                    {lesson.bagrut}
                </Markdown>
            </Typography>

            <Typography variant={'h4'}>
                Discussion
            </Typography>
            <Typography variant={'body2'} sx={{overflowWrap: 'break-word'}}>
                <Markdown>

                    {lesson.discussion}
                </Markdown>
            </Typography>

            <Typography variant={'h4'}>
                Writing
            </Typography>
            <Typography variant={'body2'} sx={{overflowWrap: 'break-word'}}>
                <Markdown>

                    {lesson.writing}
                </Markdown>
            </Typography>
        </Box>
    );
}

export default LessonPlan;