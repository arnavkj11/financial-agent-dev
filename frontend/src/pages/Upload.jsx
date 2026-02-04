import React, { useState, useRef } from 'react';
import api from '../services/api';
import { Upload, FileText, CheckCircle, AlertCircle, X } from 'lucide-react';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState(null); // 'success' | 'error'
  const [message, setMessage] = useState('');
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    if (selectedFile.type !== 'application/pdf') {
      setStatus('error');
      setMessage('Only PDF files are allowed.');
      return;
    }
    setFile(selectedFile);
    setStatus(null);
    setMessage('');
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setStatus(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Don't set Content-Type header manually for FormData
      // axios will automatically set it with the correct boundary
      await api.post('/documents/ingest', formData);
      setStatus('success');
      setMessage('File uploaded successfully! Processing started in background.');
      setFile(null);
    } catch (error) {
       setStatus('error');
       const errorDetail = error.response?.data?.detail;

       // Handle array of validation errors from FastAPI
       if (Array.isArray(errorDetail)) {
         setMessage(errorDetail.map(e => e.msg).join(', '));
       } else if (typeof errorDetail === 'string') {
         setMessage(errorDetail);
       } else {
         setMessage('Failed to upload file.');
       }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="container py-10 max-w-2xl animate-fade-in">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold mb-2">Upload Bank Statement</h1>
        <p className="text-[var(--text-muted)]">Upload your PDF bank statement to automatically extract transactions.</p>
      </div>

      <div className="card">
        <div 
          className={`border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center text-center transition-colors cursor-pointer ${
            file ? 'border-green-500/50 bg-green-500/5' : 'border-[var(--border)] hover:border-[var(--primary)] hover:bg-slate-800/50'
          }`}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            className="hidden" 
            accept=".pdf" 
            onChange={handleFileChange} 
          />
          
          {file ? (
             <div className="animate-fade-in">
               <FileText size={48} className="text-green-500 mb-4 mx-auto" />
               <h3 className="text-lg font-bold text-white mb-1">{file.name}</h3>
               <p className="text-sm text-[var(--text-muted)]">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
               <button 
                 onClick={(e) => { e.stopPropagation(); setFile(null); }}
                 className="mt-4 text-sm text-red-400 hover:text-red-300 underline"
               >
                 Remove file
               </button>
             </div>
          ) : (
            <>
              <div className="bg-slate-800 p-4 rounded-full mb-4">
                <Upload size={32} className="text-blue-400" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Click to upload or drag and drop</h3>
              <p className="text-sm text-[var(--text-muted)]">PDF files only (max 10MB)</p>
            </>
          )}
        </div>

        {/* Status Message */}
        {status && (
           <div className={`mt-6 p-4 rounded-lg flex items-center gap-3 ${status === 'success' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
             {status === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
             <p>{message}</p>
           </div>
        )}

        {/* Actions */}
        <div className="mt-8 flex justify-end">
          <button 
            className="btn btn-primary px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload & Process'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
