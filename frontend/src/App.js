import {
    Box,
    Button,
    ButtonBase, CircularProgress,
    Container,
    Divider,
    FormControl,
    InputLabel,
    MenuItem,
    Pagination,
    Paper,
    Select,
    Stack,
    TextField,
    Typography
} from "@mui/material";
import {useEffect, useState} from "react";
import axios from "axios";
import LessonPlan from "./PrompResults/LessonPlan";
import Markdown from "react-markdown";
import ChapterSummary from "./PrompResults/ChapterSummary";

function App() {

    const [selectedBook, setSelectedBook] = useState(null)
    const [books, setBooks] = useState([])
    const [bookText, setBookText] = useState('')
    const [bookChapter, setBookChapter] = useState(1)
    const [bookChapters, setBookChapters] = useState([])

    const [chapter, setChapter] = useState("")
    const [requiredContent, setRequiredContent] = useState('qa')
    const [promptResponse, setPromptResponse] = useState("")

    const [loadingPrompt, setLoadingPrompt] = useState(false)
    const [chapterLoading, setChapterLoading] = useState(false)

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/books').then(response => {
            setBooks(response.data)
        })
    }, []);

    useEffect(() => {
        if (selectedBook) {
            setChapterLoading(true)
            axios.post('http://127.0.0.1:5000/get_page', {
                book: selectedBook.id,
                page: bookChapter
            }).then(response => {
                setBookText(response.data)
            }).finally(() => {
                setChapterLoading(false)
            })
        }
    }, [bookChapter, selectedBook]);

    useEffect(() => {
        if (!selectedBook) return
        axios.post('http://127.0.0.1:5000/get_chapters', {'book_id': selectedBook.id}).then(response => {
            setBookChapters(response.data)
        }).finally(() => {
        })
    }, [selectedBook])

    function handleGenerate() {
        if (!selectedBook) {
            setPromptResponse("Please select a book")
            return
        }
        setLoadingPrompt(true)

        let url = 'generate_lesson_plan'
        if (requiredContent === 'qa') url = 'generate_questions'
        if (requiredContent === 'cs') url = 'generate_summary'


        axios.post(`http://127.0.0.1:5000/${url}`, {
            'book_id': selectedBook.id,
            'chapter_name': chapter
        }).then(response => {
            setPromptResponse(response.data)

        }).catch(error => {
            console.log("error")
        }).finally(() => {
            setLoadingPrompt(false)
        })
    }

    function HandleGetChapter(number) {
        axios.post()
    }

    return (
        <Box bgcolor={'lightgray'} p={0} m={0}>

            <Container>
                <Typography variant={'h2'} gutterBottom>
                    SikumAI
                </Typography>

                <Box mb={2}>
                    <Typography variant={'h3'}>
                        Library
                    </Typography>
                    <Paper elevation={3}>
                        <Box p={2} display={'flex'} gap={2} flexWrap={'wrap'}>

                            {
                                books.map(item => {
                                    return (
                                        <ButtonBase
                                            onClick={() => {
                                                setSelectedBook(item)
                                            }}
                                            sx={{
                                                "&:hover": {
                                                    transform: "scale(1.05)",
                                                    boxShadow: "0 0 10px 0 rgba(0,0,0,0.3)"
                                                }
                                            }}>
                                            <img width={100} src={'http://127.0.0.1:5000/static/' + item.image}
                                                 alt={"cover"}
                                                 style={{objectFit: "contain", borderRadius: 2}}/>
                                        </ButtonBase>
                                    )

                                })
                            }
                        </Box>
                    </Paper>
                </Box>

                <Typography variant={'h3'}>
                    Literature Overview
                </Typography>
                <Box mb={2}>
                    <Paper elevation={3}>
                        <Box p={2}>
                            <Stack direction={'row'} spacing={4} divider={<Divider orientation="vertical" flexItem/>}>
                                {
                                    selectedBook ?
                                        <img src={'http://127.0.0.1:5000/static/' + selectedBook.image} width={200}
                                             style={{objectFit: "contain", borderRadius: 5}}/>
                                        : <Box width={200} height={180}></Box>
                                }

                                <Box>
                                    {Object.entries(selectedBook ?? {}).map(([key, value]) => {
                                        return <>
                                            <Typography variant={'body2'} fontWeight={'bold'} display={"inline"}>
                                                {key}:
                                            </Typography>
                                            <Typography variant={'body2'}>
                                                {value}
                                            </Typography>
                                        </>
                                    })}
                                </Box>
                            </Stack>
                        </Box>
                    </Paper>
                </Box>

                <Typography variant={'h3'}>
                    Read The Book
                    {chapterLoading && <CircularProgress sx={{mx: 1}}/>}
                </Typography>
                <Box mb={2}>
                    <Paper>
                        <Box p={2}>
                            <Typography minHeight={100} maxHeight={500} variant={'body2'} overflow={'auto'}
                                        overflowX={'none'}>
                <pre>
                                {bookText}
                </pre>
                            </Typography>
                            <Box display={'flex'} justifyContent={'center'}>
                                <Pagination count={50} shape={'rounded'}
                                            onChange={(event, page) => setBookChapter(page)}/>
                            </Box>
                        </Box>
                    </Paper>
                </Box>

                <Typography variant={'h3'}>
                    Generate
                </Typography>
                <Box mb={1}>
                    <Paper variant={'outlined'} sx={{p: 2}}>
                        <Stack direction={'row'} spacing={2} divider={<Divider flexItem orientation={'vertical'}/>}>
                            <Box>
                                <FormControl fullWidth size={'small'} margin={'dense'}>
                                    <InputLabel id={'chapter-select'}>Select Chapter</InputLabel>
                                    <Select label={'Required Content'} size={'small'} value={chapter}
                                            onChange={(event) => {
                                                setChapter(event.target.value)
                                            }}>
                                        {
                                            bookChapters.map(chapter => {
                                                return <MenuItem value={chapter}>{chapter}</MenuItem>
                                            })
                                        }
                                    </Select>

                                </FormControl>

                                <FormControl fullWidth size={'small'} margin={'dense'}>
                                    <InputLabel id={'content-select'}>Required Content</InputLabel>
                                    <Select label={'Required Content'} value={requiredContent}
                                            onChange={(event) => setRequiredContent(event.target.value)}>
                                        <MenuItem value={'qa'}>
                                            Questions and Answers
                                        </MenuItem>
                                        <MenuItem value={'lp'}>
                                            Lesson Plan
                                        </MenuItem>
                                        <MenuItem value={'cs'}>
                                            Chapter Summary
                                        </MenuItem>
                                    </Select>

                                </FormControl>
                            </Box>
                            <Stack justifyContent={'space-between'}>
                                <Typography variant={'body1'}>
                                    Powered By &nbsp;
                                    <img src={'gemini.png'} width={100}/>
                                </Typography>
                                <Button variant={'contained'} sx={{height: 80}} onClick={() => handleGenerate()}>
                                    {loadingPrompt ?
                                        <CircularProgress color={'info'}/> :
                                        "Generate"
                                    }
                                </Button>
                            </Stack>
                        </Stack>

                    </Paper>
                </Box>
                <Box pb={5}>
                    <Paper>
                        <Box minHeight={100} p={2}>
                            <Typography variant={'body2'} sx={{overflowX: 'scroll'}}>
                                {requiredContent === 'lp' && promptResponse.result &&
                                    <LessonPlan lesson={promptResponse.result}/>
                                }
                                {requiredContent === 'cs' && promptResponse.result &&
                                    <ChapterSummary summary={promptResponse.result}/>
                                }

                            </Typography>
                        </Box>
                    </Paper>
                </Box>
            </Container>
        </Box>
    );
}

export default App;
