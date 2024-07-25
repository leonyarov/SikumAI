import React, {useEffect, useState} from 'react';
import {
    Alert,
    Box,
    Button,
    Dialog,
    DialogActions,
    DialogContent, DialogTitle,
    IconButton,
    Pagination,
    Paper,
    Tooltip
} from "@mui/material";
import {History} from "@mui/icons-material";
import Markdown from "react-markdown";
import axios from "axios";

function HistoryModal({type, book}) {
    const [open, setOpen] = useState(false)
    const [items, setItems] = useState([])
    const [selectedItem, setSelectedItem] = useState(null)
    const [itemString, setItemString] = useState("")
    function getHistory() {
        if (!book || !type) return
        axios.post('http://127.0.0.1:5000/history', {
            book_id: book.id,
            content: type,
        }).then(response => {
            setItems(response.data)
            setSelectedItem(response.data[0])
        })
    }

    useEffect(() => {
        if (!open) return
        getHistory()
    }, [open]);


    useEffect(() => {
        if (!selectedItem) return
        setItemString (Object.entries(selectedItem).map(([key, value]) => {
            return `## **${key}**: \n${value}`
        }).join("\n"))
    }, [selectedItem]);
    return (
        <Box>
                <Tooltip title={'View History'} placement={'top'}>
                    <IconButton onClick={() => setOpen(true)}>
                        <History/>
                    </IconButton>
                </Tooltip>

            <Dialog maxWidth={'lg'} fullWidth open={open} onClose={() => setOpen(false)}>
                <Box display={'flex'} justifyContent={'center'} mt={2}>

                    <Pagination count={items.length} shape={'rounded'} siblingCount={5} onChange={(e, page) => setSelectedItem(items[page -1])}/>
                </Box>
                <DialogContent sx={{minHeight: 500}}>
                    {items.length === 0 && <Alert severity={'error'}>
                        No history found
                    </Alert>}
                    <Paper elevation={3} sx={{p:2}}>

                    <Markdown>
                    {itemString}
                    </Markdown>
                    </Paper>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpen(false)}>
                        Close
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
}

export default HistoryModal;