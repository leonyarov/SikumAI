import {
    Box,
    Button,
    ButtonBase,
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

function App() {

    const [selectedBook, setSelectedBook] = useState(null)
    const [books, setBooks] = useState([])
    const [bookText, setBookText] = useState('')
    const [bookPage, setBookPage] = useState(1)
    const [pages, setPages] = useState("1")
    const [requiredContent, setRequiredContent] = useState('qa')
    const [promptResponse, setPromptResponse] = useState("")

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/books').then(response => {
            setBooks(response.data)
        })
    }, []);

    useEffect(() => {
        if (selectedBook) {
            axios.post('http://127.0.0.1:5000/get_page', {
                book: selectedBook.id,
                page: bookPage
            }).then(response => {
                setBookText(response.data)
            })
        }
    }, [bookPage, selectedBook]);

    function handleGenerate() {
        if (!selectedBook) {
            setPromptResponse("Please select a book")
            return
        }
        axios.post('http://127.0.0.1:5000/prompt', {
            book: selectedBook.id,
            pages: pages,
            type: requiredContent
        }).then(response => {
            setPromptResponse(response.data)
        }).catch(error => {
            setPromptResponse("Error")
        })
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
                </Typography>
                <Box mb={2}>
                    <Paper>
                        <Box p={2}>
                            <Typography maxHeight={500} minHeight={100} variant={'body2'} overflowY={'scroll'}>
                                {bookText}
                            </Typography>
                            <Box display={'flex'} justifyContent={'center'}>

                                <Pagination count={50} shape={'rounded'} onChange={(event, page) => setBookPage(page)}/>
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
                                <TextField label={"Lesson Plan Pages"} helperText={'e.g: 1-2, 3, 99'} size={'small'}
                                           margin={'dense'} value={pages} onChange={(event) => setPages(event.target.value)}/>
                                <FormControl fullWidth size={'small'} margin={'dense'}>
                                    <InputLabel id={'content-select'}>Required Content</InputLabel>
                                    <Select label={'Required Content'} value={requiredContent} onChange={(event) => setRequiredContent(event.target.value)}>
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
                                    Generate
                                </Button>
                            </Stack>
                        </Stack>

                    </Paper>
                </Box>
                <Box pb={5}>
                    <Paper>
                        <Box minHeight={100} p={2}>
                            <pre>
                            <Typography variant={'body2'} sx={{overflowX: 'scroll'}}>
                                {promptResponse}
                            </Typography>
                            </pre>
                        </Box>
                    </Paper>
                </Box>
            </Container>
        </Box>
    );
}

export default App;
