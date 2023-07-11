USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_SB]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SB]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_SB]
GO
/****** Object:  Table [dbo].[L56_DOD_SB]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_SB](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[SB03] [varchar](8) NULL,
	[SCD1] [varchar](3) NULL,
	[SCD2] [varchar](3) NULL,
	[SCD2_E] [int] NULL,
	[SCD4] [varchar](1) NULL,
	[SCD5] [varchar](1) NULL,
	[SCD3] [varchar](1) NULL,
	[SCD6] [varchar](1) NULL,
 CONSTRAINT [PK_DOD_SB_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO