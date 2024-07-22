import React from 'react';
import Markdown from "react-markdown";
import {Box, Typography} from "@mui/material";

function ChapterSummary({summary}) {
    return (
        <Box>

                {Object.entries(summary).map(([key, value]) => {
                    if (key === 'id' || key === 'chapter_name' || key === 'chapter_number' || key === 'book_name') return <></>
                    key = key.replace(/_/g, ' ')

                    return <React.Fragment key={key}>
                        <Markdown>
                            {[`### **${key}**`, value].join(":\n")}
                        </Markdown>
                    </React.Fragment>

                })}

        </Box>
    );
}

export default ChapterSummary;