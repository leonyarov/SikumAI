import React from 'react';
import Markdown from "react-markdown";
import {Box} from "@mui/material";

function ChapterSummary({summary}) {
    return (
        <Box>
            <Markdown>
                {summary.conflicts}
            </Markdown>
        </Box>
    );
}

export default ChapterSummary;