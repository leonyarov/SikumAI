import {
    Alert,
    Box,
    Button,
    ButtonBase, Chip, CircularProgress,
    Container,
    Divider,
    FormControl, IconButton,
    InputLabel, List, ListItem,
    MenuItem,
    Pagination,
    Paper,
    Select, Skeleton,
    Stack,
    TextField, Tooltip,
    Typography
} from "@mui/material";
import {useEffect, useState} from "react";
import axios from "axios";
import LessonPlan from "./PrompResults/LessonPlan";
import ChapterSummary from "./PrompResults/ChapterSummary";
import {Document, Page} from "react-pdf";
import {pdfjs} from 'react-pdf';
import {Api, AutoStories, Book, History, LibraryBooks, Textsms} from "@mui/icons-material";
import QnA from "./PrompResults/QnA";
import HistoryModal from "./PrompResults/HistoryModal";
import NewBook from "./NewBook";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
    'pdfjs-dist/build/pdf.worker.min.mjs',
    import.meta.url,
).toString();

function App() {

    const [selectedBook, setSelectedBook] = useState(null)
    const [books, setBooks] = useState([])
    const [bookLink, setBookLink] = useState('')
    const [bookChapters, setBookChapters] = useState([])

    const [pdfPageIndex, setPdfPageIndex] = useState(1)
    const [pdfPageCount, setPdfPageCount] = useState(0)

    const [chapter, setChapter] = useState("")
    const [requiredContent, setRequiredContent] = useState('qa')
    const [promptResponse, setPromptResponse] = useState("")

    const [loadingPrompt, setLoadingPrompt] = useState(false)
    const [chapterLoading, setChapterLoading] = useState(false)

    const [generateButtonText, setGenerateButtonText] = useState("Generate")

    useEffect(() => {
        if (!loadingPrompt) return

             const names = ["Generating", "Collecting Chapters", "Analyzing","Saving to DB", "Processing", "Prompting API", "Saving Results" ]
         names.forEach((name) => {
             //random time
                setTimeout(() => {
                setGenerateButtonText(name)
                }, Math.floor(Math.random() * (10000)) + 3000)
            })

    }, [loadingPrompt]);

    document.title = "SikumAI"

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/books').then(response => {
            setBooks(response.data)
        })
    }, []);

    useEffect(() => {
        if (selectedBook) {
            setChapterLoading(true)
            axios.post('http://127.0.0.1:5000/get_book', {
                book_id: selectedBook.id,
            }).then(response => {
                setBookLink(response.data)

            }).finally(() => {
                setChapterLoading(false)
            })
        }
    }, [selectedBook]);

    useEffect(() => {
        if (!selectedBook) return
        axios.post('http://127.0.0.1:5000/get_chapters', {'book_id': selectedBook.id}).then(response => {
            setBookChapters(response.data)
        }).finally(() => {
        })
    }, [selectedBook])

    function onDocumentLoadSuccess({numPages}) {
        setPdfPageCount(numPages);
    }

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
                <Box display={'flex'} justifyContent={'center'} py={2}>

                    <img width={400} src={'/logo.png'}/>
                </Box>

                <Box mb={2}>
                    <Typography variant={'h3'}>
                        Library <LibraryBooks fontSize={'large'} color={'info'}/>
                    </Typography>
                    <Paper elevation={3}>
                        <Box p={2} display={'flex'} gap={2} flexWrap={'wrap'}>

                            {
                                books.map(item => {
                                    return (
                                        <Tooltip title={item.title} placement={'top'} sx={{fontSize: 30}}>

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
                                        </Tooltip>
                                    )

                                })
                            }

                           <NewBook/>
                        </Box>
                    </Paper>
                </Box>

                <Typography variant={'h3'}>
                    Literature Overview <Book fontSize={'large'} color={'info'}/>
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

                                <List dense>
                                    {Object.entries(selectedBook ?? {}).map(([key, value]) => {
                                        return <ListItem>
                                            <Chip label={key} size={'small'}
                                                  sx={{textTransform: 'capitalize', fontWeight: 'bold'}}/>
                                            <Typography display={'inline'} variant={'body2'} sx={{ml: 1}}>
                                                {value}
                                            </Typography>
                                            <br/>
                                        </ListItem>
                                    })}
                                </List>
                            </Stack>
                        </Box>
                    </Paper>
                </Box>

                <Typography variant={'h3'}>
                    Read The Book <AutoStories fontSize={'large'} color={'info'}/>
                    {chapterLoading && <CircularProgress sx={{mx: 1}}/>}
                </Typography>
                <Box mb={2}>
                    <Paper>
                        <Box p={2}>
                            <Stack justifyContent={'center'} alignItems={'center'}>

                                <Document file={`http://127.0.0.1:5000/static/books/${bookLink}`}
                                          onLoadSuccess={onDocumentLoadSuccess}
                                          error={<Alert severity={'info'}>Could not load PDF</Alert>}
                                          loading={<Skeleton variant="rectangular" width={500} height={600}/>}
                                >
                                    <Paper elevation={3}>
                                        <Page pageNumber={pdfPageIndex} renderAnnotationLayer={false}
                                              renderTextLayer={false}/>
                                    </Paper>
                                </Document>

                                <Pagination sx={{my: 2}} count={pdfPageCount} shape={'rounded'}
                                            onChange={(event, page) => setPdfPageIndex(page)}/>
                            </Stack>
                        </Box>
                    </Paper>
                </Box>

                <Typography variant={'h3'}>
                    Generate <Textsms fontSize={'large'} color={'info'}/>
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
                                <Button disabled={loadingPrompt} variant={'contained'} sx={{height: 80}} onClick={() => handleGenerate()}  >
                                    {loadingPrompt ?
                                        <> {generateButtonText} <CircularProgress color={'info'}/></>  :
                                        "Generate"
                                    }
                                </Button>
                            </Stack>
                            <HistoryModal type={requiredContent} book={selectedBook}/>
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
                                {requiredContent === 'qa' && promptResponse.result &&
                                    <QnA/>
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
