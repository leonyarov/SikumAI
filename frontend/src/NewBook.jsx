import React, {useState} from 'react';
import {
    Box,
    Button,
    ButtonBase,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle, styled,
    TextField,
    Tooltip, Typography
} from "@mui/material";
import {Bookmark, ImageSearch} from "@mui/icons-material";
import axios from "axios";

const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
});


function NewBook(props) {
    const [open, setOpen] = useState(false)
    const [bookUpload, setBookUpload] = useState("")
    const [coverUpload, setCoverUpload] = useState("")

    const handleCoverChange = (e) => {
        if (e.target.files) {
            setCoverUpload(e.target.files[0]);
        }
    };

    const handleBookChange = (e) => {
        if (e.target.files) {
            setBookUpload(e.target.files[0]);
        }
    }

    function formUpload(e) {
        e.preventDefault()
        axios.post('http://127.0.0.1:5000/upload_book', new FormData(e.target)).then((res) => {
            console.log("a")
        })
    }

    return (
        <Box>
            <Tooltip title={"New Book"} placement={'top'} sx={{fontSize: 30}}>

                <ButtonBase
                    onClick={() => {
                        setOpen(true)
                    }}
                    sx={{
                        "&:hover": {
                            transform: "scale(1.05)",
                            boxShadow: "0 0 10px 0 rgba(0,0,0,0.3)"
                        }
                    }}>
                    <img width={100} src={'http://127.0.0.1:5000/static/newbook.png'}
                         alt={"cover"}
                         style={{objectFit: "contain", borderRadius: 2}}/>
                </ButtonBase>
            </Tooltip>
            <Dialog open={open} onClose={() => setOpen(false)} fullWidth>
                <DialogTitle>
                    Add New Book
                </DialogTitle>
                <DialogContent>
                    <form id={'book_upload'} onSubmit={formUpload}>

                        <Box sx={{display: 'flex', flexDirection: 'column', gap: 2}}>
                            {/* author,image, msdn,pages,short_text,title,*/}
                            <TextField name={'author'} placeholder={"Author"} fullWidth required/>
                            <TextField name={'title'} placeholder={"Title"} fullWidth required/>
                            <TextField name={'msdn'} placeholder={"MSDN"} fullWidth/>
                            <TextField name={'short_text'} placeholder={"Short Text"} fullWidth multiline rows={2}/>
                            <Button
                                component="label"
                                role={undefined}
                                variant="contained"
                                tabIndex={-1}
                                startIcon={<Bookmark/>}
                            >
                                Upload Book file
                                <VisuallyHiddenInput name={'book'} type="file" onChange={handleBookChange} accept={'.pdf'}/>
                            </Button>
                            <Typography variant={'caption'}>
                                {bookUpload.name}
                            </Typography>
                            <br/>
                            <Button
                                component="label"
                                role={undefined}
                                variant="contained"
                                tabIndex={-1}
                                startIcon={<ImageSearch/>}
                            >
                                Upload Book Cover
                                <VisuallyHiddenInput name={'cover'} type="file" onChange={handleCoverChange} accept={'image/*'}/>
                            </Button>
                            <Typography variant={'caption'}>
                                {coverUpload.name}
                            </Typography>
                        </Box>
                    </form>

                </DialogContent>
                <DialogActions>
                    <Button variant={'success'} form={'book_upload'} type={'submit'}>
                        Add
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
}

export default NewBook;